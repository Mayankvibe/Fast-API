from pydantic import (BaseModel ,Field ,field_validator,model_validator ,computed_field,EmailStr)
from typing import Annotated , Optional
from uuid import UUID
from datetime import datetime

#CREATE PYDANTIC

class DimensionsCM(BaseModel):
     length:Annotated[
        float,
        Field( gt=0, strict=True, description="Length in cm"
        )]
     
     width:Annotated[
        float,
        Field(
           gt=0, strict=True, description="width in cm"
        )]
     
     height:Annotated[
        float,
        Field(
           gt=0, strict=True, description="height in cm"
            
        )]


class Seller(BaseModel):
     
     id: UUID
    
     name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Name of the seller (2-60 chars).",
            examples=["Mi Store", "Apple Store India"],
        ),
    ]
     email:EmailStr

     @field_validator("email",mode="after")
     @classmethod
     def seller_email_validate(cls, value:EmailStr):
          if "@" not in value:
               raise ValueError("email have must'@'")
          last=value.split("@")[-1].lower()
          allow_domain={"mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "hpworld.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexclusive.in",}
          if last not in allow_domain :
               raise ValueError(f"seller eamil domain not allowed:{last} ")
          return value


class Product(BaseModel):
     
     id: UUID
     sku: Annotated[ str , Field(
          min_length=5,
          max_length=17,
          description="unit size",
          title="SKU",
          example="REAL-170GB-092"
     )]
     name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="product  Name",
            description="Name of the product (2-60 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]
     created_at:datetime
     discount_percent: Annotated[
        int,
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ] = 0
     price: Annotated[float, Field(gt=0, strict=True, description="Base price (INR)")]

     stock:int
     seller:Seller
     dimensions_cm: DimensionsCM
     created_at:datetime

     @field_validator("sku",mode="after")
     @classmethod
     def sku_validate(cls, value:str):
          if "-" not in value:
               raise ValueError("sku have must'-'")
          last=value.split("-")[-1] 
          if not (len(last)==3 and last.isdigit()):
               raise ValueError("sku last 3 digit end with like '-456' ")
          return value
       
     @computed_field
     @property
     def final_price(self) -> float :
        return round(self.price * (1-self.discount_percent/100),2)
     
     @computed_field
     @property
     def dimension_volume(self) -> float :
        s=self.dimensions_cm
        return round(s.length*s.width*s.height,2)
     

# UPDATE PYDANTIC

class DimensionsCMupdate(BaseModel):
     length:Annotated[
        Optional[float],
        Field(
            gt=0, strict=True, description="Length in cm"
        )]
     
     width:Annotated[
        Optional[float],
        Field(
           gt=0, strict=True, description="width in cm"
        )]
     
     height:Annotated[
        Optional[float],
        Field(
           gt=0, strict=True, description="height in cm"
            
        )]


class Sellerupdate(BaseModel):
     
     id: UUID
    
     name: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Name of the seller (2-60 chars).",
            examples=["Mi Store", "Apple Store India"],
        ),
    ]
     email:Optional[EmailStr]

     @field_validator("email",mode="after")
     @classmethod
     def seller_email_validate(cls, value:EmailStr):
          if "@" not in value:
               raise ValueError("email have must'@'")
          last=value.split("@")[-1].lower()
          allow_domain={"mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "hpworld.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexclusive.in",}
          if last not in allow_domain :
               raise ValueError(f"seller eamil domain not allowed:{last} ")
          return value


class Productupdate(BaseModel):
     
     id: UUID
     sku: Annotated[ Optional[str] , Field(
          min_length=5,
          max_length=17,
          description="unit size",
          title="SKU",
          example="REAL-170GB-092"
     )]
     name: Annotated[
        Optional[str],
        Field(
            min_length=2,
            max_length=60,
            title="product  Name",
            description="Name of the product (2-60 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]
   
     discount_percent: Annotated[
        Optional[int],
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ] = 0
     price: Annotated[Optional[float], Field(gt=0, strict=True, description="Base price (INR)")]

     stock:Optional[int]
     seller:Optional[Sellerupdate]
     dimensions_cm: Optional[DimensionsCMupdate]
     created_at:datetime

     @field_validator("sku",mode="after")
     @classmethod
     def sku_validate(cls, value:str):
          if "-" not in value:
               raise ValueError("sku have must'-'")
          last=value.split("-")[-1] 
          if not (len(last)==3 and last.isdigit()):
               raise ValueError("sku last 3 digit end with like '-456' ")
          return value
       
     @computed_field
     @property
     def final_price(self) -> float :
        return round(self.price * (1-self.discount_percent/100),2)
     
     @computed_field
     @property
     def dimension_volume(self) -> float :
        s=self.dimensions_cm
        return round(s.length*s.width*s.height,2)
     