
from fastapi import FastAPI,Query,HTTPException,Path
from products import get_all_products
from schema.product_pydantic import Product,Productupdate
from uuid import uuid4,UUID
from datetime import datetime
from products import add_product,remove_product,change_product
app = FastAPI()



@app.get("/")
def root():    
    return {"message": "hyyy"}
#def get_products():
 #   return get_all_products()


@app.get("/products")
def list_products(
     
     
        name:str =Query(
            default=None,
            min_length=1,
            max_length=50,
            description="search by product name(case insensitive)",
        ),
        sort_by_price:bool=Query(
             default=False,
             description="product  is sort by the price"
        ),
        order:str=Query(
             default="asc",description="sort order if sort_by_price=true (asc,desc)"
        ),
        limit:int=Query(
             default=5,
             ge=1,
             le=100,
             description="number of user"
        ),
        offset:int=Query(
             default=0,
             ge=0,
             description="show thw next page"
        )
):
    products=get_all_products()
    if name:
        neeedle=name.strip().lower()
        products=[p for p in products if neeedle in p.get("name" ,"").lower()]

    if not products:
            raise HTTPException(status_code=404,detail=f"no product found matching name={name}")  

    if sort_by_price:
        reverse= order=="desc"  
        products= sorted( products , key=lambda p:p.get("price",0), reverse=reverse ) 

    total=len(products)
    products=products[offset:offset+limit]
    return {"total":total,"limit":limit,"item":products}


@app.get("/products/{product_id}")
def get_product_id(product_id:str=Path(...,
        min_length=36,
        max_length=36,
        description="uuid of products",
        example="2cac1c2a-9692-0000-97b3-6bbf9dc615c0"
                        )):
   products=get_all_products()
   for product in products:
        if product["id"]==product_id:
             return product
   raise HTTPException(status_code=404,detail=f"there is no produtc")
 

@app.post("/products", status_code=201)
def create(product:Product):
     products_dict=product.model_dump(mode="json")
     products_dict["id"]=str(uuid4())
     products_dict["created_at"]=datetime.utcnow().isoformat()+"Z"
     try:
          add_product(products_dict)
     except ValueError as e:
          raise HTTPException(status_code=400,detail=str(e))
     return product.model_dump(mode="json")


@app.delete("/products/{product_id}")
def delete_product(product_id:UUID=Path(...,description="Product UUID")):
     try:
          reso=remove_product(product_id)
          return reso
     except Exception as e:
          raise HTTPException(status_code=400,detail=str(e))
      
@app.put("/products/{product_id}")
def update_product(product_id:UUID=Path(...,description="Product UUID"),payload:Productupdate=...):
     try:
          update_=change_product(product_id,payload.model_dump(mode="json",exclude_unset=True))
          return update_
     except ValueError as e:
          raise HTTPException(status_code=400,detail=str(e))