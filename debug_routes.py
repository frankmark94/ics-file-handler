from app import app

print("Registered routes in the Flask application:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}") 