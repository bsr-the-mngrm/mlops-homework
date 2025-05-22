import kagglehub

# Download latest version
path = kagglehub.dataset_download("airbnb/seattle")

print("Path to dataset files:", path)