from app.database.supabase import supabase


response = supabase.table("creators").select("*").limit(1).execute()


print("Supabase connection successful!")

print(response.data)
