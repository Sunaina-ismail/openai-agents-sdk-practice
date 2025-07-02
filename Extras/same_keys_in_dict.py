from typing import Dict

fruits: list[Dict[str, str]] = [
    {
        "name": "apple",
        "taste": "sweeet"
    },
    {
        "name": "apple",
        "taste": "sour"
    },
    {
        "name": "apple",
        "taste": "bitter"
    }
]

fruit_dict: Dict[str, str] = {fruit['name']: fruit['taste'] for fruit in fruits}
print(fruit_dict)

#! Output: {'apple': 'bitter'}
#! isliye q k name same ha to first iteration pr key set hogi or then phr har iteration pr us same key ki value iterate hogi.
#! Isliye final value last index waly element ki consider ki jayega

#? Same senario tool_calling ma bh hota ha, agar ham same name k sath multiple tool de den with same parameters to hamesha last wala tool call hota ha 