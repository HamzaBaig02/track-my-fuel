class SupabaseAPIError(Exception):
    def __init__(self, message="Supabase API error"):
        self.message = message
        super().__init__(self.message)
