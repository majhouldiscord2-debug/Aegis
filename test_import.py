print("Test script started")
import sys
print(f"Python version: {sys.version}")
print("Trying to import aegis...")
try:
    from aegis import AegisSystem
    print("Aegis imported successfully")
    print("Creating AegisSystem...")
    system = AegisSystem()
    print("AegisSystem created successfully")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
print("Test complete")
