Common subdirectories: ./__pycache__ and /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi/__pycache__
Only in /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi: automodapi.py~
diff -u ./automodsumm.py /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi/automodsumm.py
--- ./automodsumm.py	2019-09-05 09:34:24.000000000 +0200
+++ /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi/automodsumm.py	2019-08-31 09:35:17.000000000 +0200
@@ -492,6 +492,8 @@
 
         new_files.append(fn)
 
+        # fn = re.sub(r'([A-Z])',r'\1_',fn)  # DTW
+        fn = fn.replace("DTW","D_T_W_")
         f = open(fn, 'w')
 
         try:
Only in /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi: automodsumm.py~
Common subdirectories: ./templates and /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi/templates
Common subdirectories: ./tests and /Users/toni/anaconda3-backup/lib/python3.6/site-packages/sphinx_automodapi/tests
