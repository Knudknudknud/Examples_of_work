from typing import List,Any, Optional
import random

class Utils():
    
    @staticmethod
    def pick_item(items:List[Any],weighted_item:Any = None,weight:float = 1)->Optional[Any]:
        """
        Picks an item from a list of items, a specific item can be given a different weight.

        Args:
            items: List[Any] - List of items to pick from.
            weighted_item: Any - The item to give a different weight.
            weight: float - The weight to give the weighted item.
        Returns:
            item (Any): The picked item. 
            None: If the list is empty.
        Raises:
            ValueError: If the weight is negative.
        """
        if weight < 0:
            raise ValueError('Weight must be non-negative')
        if not items:
            return None
        
        weights = [weight if item == weighted_item else 1.0 for item in items]

        return random.choices(items, weights=weights, k=1)[0]
