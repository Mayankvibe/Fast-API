import json 
from pathlib import Path 
from typing import List , Dict

DATA_FILE=Path(__file__).parent/"data"/"dummy.json"



def load_product() -> List[Dict]:
    if not DATA_FILE.exists():
        return[]
    with open(DATA_FILE,"r",encoding="utf-8") as file:
        return json.load(file)
    
def get_all_products() -> List[Dict]:
    return load_product()   

def save_products(product:List[dict]) -> None :
     with open(DATA_FILE,"w",encoding="utf-8") as f:
         json.dump(product , f,indent=2,ensure_ascii=False)

def add_product(product:dict):
    products=get_all_products()
    if any(p["sku"]==product["sku"]  for p in products):
        raise ValueError("sku is already exist")
    products.append(product)
    save_products(products)
    return product
       
def remove_product(id:str) -> str:
    products=get_all_products()
    for index,p in enumerate(products):
        if p["id"]==str(id):
            deleted=products.pop(index) 
            save_products(products)
            return {"message":"product deleted sucessfully !" ,"data":deleted}      
        

def change_product(product_id:str,update_data:dict):
    products=get_all_products()
    for index,product in enumerate(products):

        for key,value in update_data.item():
            if value is None:
                continue

            if isinstance(value,dict) and isinstance(product.get(key),dict):
                product[key].update(value)
            else:
                    product[key]=value
            
            products[index]=product
            save_products(product)
            return product
        raise ValueError("product not found")    




