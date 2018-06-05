import zipfile
from pathlib import Path
import os
import shutil
import xml.etree.ElementTree as ET

#WriteImage
with open("./ImageURL.txt", "w") as f:
    f.write('')

# Get Current Directory
sourcePath = Path(os.getcwd())

# Create zipCollection Direction
zipCollectionDir = "ZipCollection"
if not os.path.exists(os.path.join(sourcePath,zipCollectionDir)):
    os.makedirs(os.path.join(sourcePath,zipCollectionDir))

# Create Result Direction
resultZip = "result"
if not os.path.exists(os.path.join(sourcePath,resultZip)):
    os.makedirs(os.path.join(sourcePath,resultZip))

# Extract File
for file in os.listdir(sourcePath):
    if file.endswith(".zip"):
        zipFilePath = os.path.join(sourcePath,file)
        result = zipfile.ZipFile(zipFilePath)
        result.extractall(os.path.join(sourcePath,zipCollectionDir))

# Zip Directory Path
zipDirPath = os.path.join(sourcePath,zipCollectionDir)

# Delete Unwanted Directory
for file in os.listdir(os.path.join(sourcePath,zipCollectionDir)):
    if file.startswith("_"):
        shutil.rmtree(os.path.join(zipDirPath,file))


# Loop to find .idml file and change it to zip
for file in os.listdir(zipDirPath):
    parentDir = os.path.join(zipDirPath,file)
    for insidefile in os.listdir(parentDir):
        if insidefile.endswith(".idml"):
            preffix,suffix = insidefile.split('.')
            os.rename(parentDir+"/"+insidefile,parentDir+"/"+preffix+".zip")
            zip = zipfile.ZipFile(parentDir+"/"+preffix+".zip")

            #Create each result directory
            if not os.path.exists(os.path.join(sourcePath, resultZip) + "/" + preffix):
                os.makedirs(os.path.join(sourcePath, resultZip) + "/" + preffix)
            zip.extractall(os.path.join(sourcePath, resultZip) + "/" + preffix)


#Result Directory Path
result = os.path.join(sourcePath,resultZip)

# #Loop through XML to find  JPG / EPS / PSD
for file in os.listdir(result):
    rootDir = os.path.join(result,file)
    for subfile in os.listdir(rootDir):
        if subfile.startswith("META-INF"):
            childDir = os.path.join(rootDir,subfile)
            for metaFile in os.listdir(childDir):
                if metaFile.startswith("meta"):
                    tree = ET.parse(childDir + "/" +metaFile)
                    root = tree.getroot()
                    for subtree1 in root:
                        print("RDF",subtree1)
                        for subtree2 in subtree1:
                            print("DES",subtree2)
                            for manifest in subtree2.findall("{http://ns.adobe.com/xap/1.0/mm/}Manifest"):
                                print("Manifest",manifest)
                                for subMan in manifest:
                                    print("Manifest-Bag",subMan)
                                    for manBag in subMan:
                                        print("Bag-li",manBag)
                                        for bagli in manBag.findall("{http://ns.adobe.com/xap/1.0/sType/ManifestItem#}reference"):
                                            print("reference",bagli.tag)
                                            for reference in bagli.findall("{http://ns.adobe.com/xap/1.0/sType/ResourceRef#}lastURL"):
                                                with open("./ImageURL.txt","a") as f:
                                                    f.write(reference.text + '\n')


                            for ingredient in subtree2.findall("{http://ns.adobe.com/xap/1.0/mm/}Ingredients"):
                                print("ingredient",ingredient)
                                for ingreBag in ingredient:
                                    print("ingre-bag",ingreBag)
                                    for li in ingreBag:
                                        print("ingre-li",li)
                                        for ingrefilepath in li.findall("{http://ns.adobe.com/xap/1.0/sType/ResourceRef#}filePath"):
                                            with open("./ImageURL.txt", "a") as f:
                                                f.write(ingrefilepath.text + '\n')
