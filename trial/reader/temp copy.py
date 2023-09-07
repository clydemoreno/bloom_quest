import sys
# sys.path.append("../messaging")


from pathlib import Path

sys.path.append('./async')


parent_dir = Path(__file__).resolve().parent
# Add the 'messaging' directory to sys.path
print ("here ", parent_dir.parent)
