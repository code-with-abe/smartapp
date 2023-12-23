
import uuid
import os

uploaded_file = "test.csv"
        
        # Generate a new filename with a standard prefix and random UUID
_, file_extension = os.path.splitext(uploaded_file)
new_file_name = f"med780g_{uuid.uuid4()}{file_extension}"
print(new_file_name)