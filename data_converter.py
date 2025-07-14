import pandas as pd
import json


df = pd.read_csv("Nugget_New_feature_dataset.csv")

menu_items = []

for _, row in df.iterrows():
    metadata = {
        "category": str(row.get('category', '')),
        "name": str(row.get('name', '')),
        "price": str(row.get('price', '')),
        "description": str(row.get('description', '')),
        "veg_nonveg": str(row.get('veg_nonveg', '')),
        "spice_level": str(row.get('spice_level', '')),
        "restaurant name": str(row.get('restaurant name', '')),
        "location": str(row.get('location', '')),
        "contact": row.get('contact', ''),
        "operating hour": str(row.get('operating hour', '')),
        "dining rating": float(row.get('dining rating', 0)) if pd.notnull(row.get('dining rating', '')) else None,
        "delivery rating": float(row.get('delivery rating', 0)) if pd.notnull(row.get('delivery rating', '')) else None,
        "dish type": str(row.get('dish type', ''))
    }
    
    page_content = (
        f"restaurant name: {metadata['restaurant name']} | "
        f"location: {metadata['location']} | "
        f"operating hour: {metadata['operating hour']} | "
        f"category: {metadata['category']} | "
        f"name: {metadata['name']} | "
        f"price: {metadata['price']} | "
        f"description: {metadata['description']} | "
        f"veg_nonveg: {metadata['veg_nonveg']} | "
        f"spice_level: {metadata['spice_level']} | "
        f"dish type: {metadata['dish type']} | "  # Insert dish_type here
        f"contact: {metadata['contact']} | "
        f"dining rating: {metadata['dining rating']} | "
        f"delivery rating: {metadata['delivery rating']}"
    )

    item = {
        "id": None,
        "metadata": metadata,
        "page_content": page_content,
        "type": "Document"
    }
    
    menu_items.append(item)

with open("Nugget_restaurant_menu.json", "w", encoding="utf-8") as f:
    json.dump(menu_items, f, ensure_ascii=False, indent=2)

print("Saved as Nugget_restaurants_menu.json")