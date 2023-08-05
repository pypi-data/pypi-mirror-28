# imgcompare

use pillow to compare two image

step 1 : 
	compare two image.resize
	if false ; resize
step 2 : 
	compare two image
	or 
    get per 


## Dependencies

* Pillow ( )https://python-pillow.org/ )

## Usage

### compare images


### get the diff percentage

    percentage = image_diff_percent(Image.open("1.png"), Image.open("2.png"))

	or 
	
	percentage = image_diff_percent("1.png", "2.png")
 
    same = is_equal("1.png", "2.png", tolerance=0.0)
    
	same = is_equal("1.png", "2.png", tolerance=0.5)

## Examples


## License

MIT License
