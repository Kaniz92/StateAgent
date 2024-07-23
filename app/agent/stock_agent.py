from pydantic import Field
from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar, Dict
from pydantic import BaseModel
from app.tool.ToolAdapter import ToolAdapter


class StockTickerPriceInput(BaseModel):
    ticker: str = Field(..., description='The ticker symbol of the stock')


class StockTickerPriceOutput(BaseModel):
    price:float = Field(..., description= 'The current price of the stock')


class StockTickerPrice(ToolAdapter):
    name = 'StockTickerPrice'
    description = 'Gets the current price for a Stock ticker'

    def execute(self, inputs: StockTickerPriceInput) -> StockTickerPriceOutput:
        return StockTickerPriceOutput(price=0.0)

    def schema(self):
        return{
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': StockTickerPriceInput.schema_json()
            }
        }
