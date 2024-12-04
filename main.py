import os
import logging
import yfinance as yf
import gradio as gr
from pydantic import BaseModel
from pydantic_ai import Agent

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get API key from environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY environment variable not set")
    raise ValueError("GROQ_API_KEY environment variable not set")

class StockPriceResult(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    message: str

stock_agent = Agent(
    "groq:llama3-groq-70b-8192-tool-use-preview",
    result_type=StockPriceResult,
    system_prompt="""You are a helpful financial assistant that can look up stock prices. 
    Extract the stock symbol from the query and use the get_stock_price tool to fetch current data.
    For oil prices, use 'USO' as the symbol."""
)

@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the current stock price for a given symbol.
    
    Args:
        symbol (str): The stock symbol to look up
        
    Returns:
        dict: Contains price and currency information
        
    Raises:
        ValueError: If the stock symbol is invalid or price cannot be fetched
    """
    try:
        logger.info(f"Fetching price for symbol: {symbol}")
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.last_price
        
        if price is None:
            raise ValueError(f"No price data found for symbol: {symbol}")
            
        return {
            "price": round(price, 2),
            "currency": "USD"
        }
    except Exception as e:
        logger.error(f"Error fetching stock price for {symbol}: {str(e)}")
        raise

def get_stock_info(query: str) -> str:
    """
    Process a natural language query about stock prices.
    
    Args:
        query (str): The user's question about stock prices
        
    Returns:
        str: Formatted response with stock information
    """
    try:
        logger.info(f"Processing query: {query}")
        result = stock_agent.run_sync(query)
        response = f"Stock: {result.data.symbol}\n"
        response += f"Price: ${result.data.price:.2f} {result.data.currency}\n"
        response += f"\n{result.data.message}"
        return response
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

# Create Gradio interface
demo = gr.Interface(
    fn=get_stock_info,
    inputs=gr.Textbox(label="Ask about any stock price", placeholder="What is Apple's current stock price?"),
    outputs=gr.Textbox(label="Stock Information"),
    title="Stock Price AI Assistant",
    description="Ask me about any stock price and I'll fetch the latest information for you!"
)

if __name__ == "__main__":
    logger.info("Starting Stock Price AI Assistant")
    demo.launch()