import json

from django.http                    import HttpResponse, JsonResponse
from django.views                   import View
from django.db.models               import Count, F

from .models                        import Product, Category, SubCategory
from lush_settings                  import LIST_COUNT
        
def make_product_list(lists):
    product_list = [
        {
        "product_name"      :product.name,
        "product_number"    :product.product_number,
        "is_new"            :product.is_new,
        "is_vegan"          :product.is_vegan,
        "hash_tag"          :product.hash_tag,
        "price"             :int(product.price),
        "stock"             :product.stock,
        "image"             :product.thumbnail_image.first().url,
        "sub_category_name" :product.sub_category.name,
        "sub_category_code" :product.sub_category.code
        }
        for product in lists
    ]
    return product_list

class ProductListView(View):
    def get(self, request):
        page = int(request.GET.get("page",1))
        category_code = request.GET.get("category_code")
        
        product_count = LIST_COUNT
        limit = product_count * page
        offset = limit - product_count
        all_products = Product.objects.all().prefetch_related(
            "thumbnail_image"
        ).select_related(
            "sub_category"
        )[offset:limit]

         # Category 기준 카운트
        total_category = Product.objects.values(
            "sub_category__category__name",
            "sub_category__category__code",
        ).annotate(
            category_name = F("sub_category__category__name"),
            category_code = F("sub_category__category__code"),
            total = Count("category_name"),
        )
        # Sub_category 기준 카운트            
        total_sub_category = Product.objects.values(
            "sub_category__name",
            "sub_categry__code",
        ).annotate(
            category_name = F("sub_category__name"),
            category_code = F("sub_category__code"),
            total = Count("category_name")
        ) 
        
        try :
            # Category 전체 기준 리스트
            if Category.objects.filter(code = category_code).exists():
                all_products = Product.objects.all().prefetch_related(
                    "thumbnail_image"
                ).select_related(
                    "sub_category"
                )[offset:limit]
                product_list = make_product_list(all_products)
                return JsonResponse(
                    {
                        "product":product_list,
                        "count":list(total_category)+list(total_sub_category)
                    }, 
                    status=200
                )
            
            # Sub_category 기준 리스트
            sub_category_products = Product.objects.filter(
                sub_category__code = category_code
            )[offset:limit]
            product_list = make_product_list(sub_category_products)

            return JsonResponse(
                {
                    "product":product_list,
                    "count":list(total_category)+list(total_sub_category)
                },
                status = 200
            )
        except:
            return HttpResponse(status=400)

class ProductDetailView(View):
    def get(self, request, product_id):
        detail_info = {}
        product_detail = Product.objects.filter(
            product_number=product_id
        ).prefetch_related(
            "thumbnail_image"
        ).prefetch_related(
            "weight"
        ).prefetch_related(
            "related_products"
        ).select_related(
            "detail"
        ).first()
        detail_info["product_name"] = product_detail.name 
        detail_info["hash_tag"]     = product_detail.hash_tag
        detail_info["image"]        = product_detail.thumbnail_image.first().url
        detail_info["price"]        = int(product_detail.price)
        detail_info["weight"]       = product_detail.weight.first().weight_g
        detail_info["extra_price"]  = int(product_detail.weight.first().extra_price)
        detail_info["video"]        = product_detail.detail.video_url
        detail_info["html"]         = product_detail.detail.html
        
        # related_product 따로 추출
        related_products_id         = [product.to_product_id for product in product_detail.to_product.all()]
        related_products            = [Product.objects.get(id=i) for i in related_products_id]
        detail_info["related"]      = make_product_list(related_products)
        
        return JsonResponse(
            {
            "detail":detail_info,
            },
            status=200
        )
