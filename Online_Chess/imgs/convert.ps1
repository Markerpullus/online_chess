$imgs = Get-ChildItem -Filter *.png
foreach ($img in $imgs) {
magick convert $img.FullName -strip $img.FullName
}