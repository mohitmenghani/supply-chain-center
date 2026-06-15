import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Ensure reproducibility
np.random.seed(42)
random.seed(42)

def build_dataset():
    skus = ["SKU-MICROCHIPS-77X", "SKU-LITHIUM-CELLS", "SKU-STEEL-FASTENERS"]
    categories = ["Electronics", "Automotive", "Hardware"]
    regions = ["US-East", "US-West", "EMEA", "APAC"]
    
    suppliers = {
        "SKU-MICROCHIPS-77X": {"name": "TSMC-Partner (Taiwan)", "lead": 45},
        "SKU-LITHIUM-CELLS": {"name": "GigaPower (Vietnam)", "lead": 30},
        "SKU-STEEL-FASTENERS": {"name": "MexiSteel (Mexico)", "lead": 12}
    }
    
    data = []
    start_date = datetime(2026, 1, 1)
    
    for _ in range(1000):
        sku = random.choice(skus)
        region = random.choice(regions)
        sup = suppliers[sku]
        
        hist_demand = random.randint(500, 1500)
        current_vol = int(hist_demand * np.random.uniform(0.8, 1.45))
        wh_load = round(random.uniform(40.0, 98.0), 2)
        
        # Simulate physical IoT sensory telemetry
        iot_temp = round(random.uniform(15.0, 42.0), 1)
        iot_shock_g = round(random.uniform(0.1, 4.5), 2)
        
        # Calculate logistics latency anomalies
        multiplier = 1.35 if region == "US-West" or sku == "SKU-MICROCHIPS-77X" else 1.0
        actual_days = int(sup["lead"] * np.random.uniform(0.9, 1.5) * multiplier)
        delay = max(0, actual_days - sup["lead"])
        
        # Structural unstructured logic for RAG
        if delay > 10 or iot_temp > 38.0:
            risk = "CRITICAL: Temperature breach or port constraints impacting thermal envelope and delivery timeline."
        elif delay > 4:
            risk = "WARNING: Route tracking shows minor processing friction at customs clearing."
        else:
            risk = "OPTIMAL: Route clear. Internal logistics metrics running nominally."
            
        metadata = f"Supplier: {sup['name']} | Current Capacity: {random.randint(70,100)}% | Node Status: {risk}"
        
        data.append({
            "Record_Date": (start_date + timedelta(days=random.randint(0, 150))).strftime("%Y-%m-%d"),
            "SKU": sku,
            "Category": categories[skus.index(sku)],
            "Destination_Region": region,
            "Historical_Avg_Demand": hist_demand,
            "Current_Order_Volume": current_vol,
            "Warehouse_Capacity_Pct": wh_load,
            "Scheduled_Transit_Days": sup["lead"],
            "IoT_Container_Temp_C": iot_temp,
            "IoT_Shock_G": iot_shock_g,
            "Days_Delayed": delay,
            "Supplier_Operational_Metadata": metadata
        })
        
    df = pd.DataFrame(data)
    df.to_csv("synthetic_intelligent_supply_chain.csv", index=False)
    print("📦 Success: Created multi-modal dataset 'synthetic_intelligent_supply_chain.csv'")

if __name__ == "__main__":
    build_dataset()