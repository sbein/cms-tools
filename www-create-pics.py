#!/bin/env python
import glob
import os
from optparse import OptionParser
from os.path import expanduser

parser = OptionParser()
(options, args) = parser.parse_args()

if len(args)>0:
    configurations = args
else:
    print("Run with \n$ ./www-create-pics.py www-subfolder path/to/folder/to/upload")
    quit()

www_folder = "plots"

output_folder = args[0]
input_folder = args[1]

# outfolder = args[-1].split("/")[-1]
# if outfolder[-1] == "/":
#     outfolder = outfolder[:-1]

home = expanduser("~")

output_path = "%s/www/%s/%s" % (home, www_folder, output_folder)

os.system("mkdir -p %s" % (output_path))
os.system("cp -r %s/* %s/" % (input_folder, output_path))

html = ""

print("globing", output_path + "/*.pdf")
print(glob.glob(output_path + "/*.pdf"))

for ifile in sorted(glob.glob(output_path + "/*.pdf")):
    if "_log.pdf" in ifile:
        continue
    print(ifile)
    outfile = ifile.split("/")[-1]
    
    os.system("convert %s/%s %s/%s" % (output_path, outfile, output_path, outfile.replace(".pdf", ".png")))
        
    html += """
    <table class="tg" style="display: inline-block;">
    <thead>
      <tr>
        <th class="tg-0lax"><center>%s</center><br><a href="%s"><img src="%s" width="400"></a></th>
      </tr>
    </thead>
    </table>
    """ % (outfile.replace(".pdf", ""), outfile, outfile.replace(".pdf", ".png"))

with open("%s/www/%s/%s/index.html" % (home, www_folder, output_folder), "w+") as fo:
    fo.write(html)

