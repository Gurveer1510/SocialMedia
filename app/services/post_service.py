class PostService:

    @staticmethod
    async def check_for_duplicate_items(ls) -> bool:
        if len(ls) != len(set(ls)):
            return False
        return True