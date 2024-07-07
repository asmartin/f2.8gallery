# f2.8gallery

An elegant and responsive static site generator for displaying your photography portfolio.

![f2.8gallery screenshot](screenshot.gif)

[Demo](https://andrewmartin.photos)

## Features

- Fast and responsive
- Interactive fullscreen image viewer
- Engaging animations and effects
- Build multiple galleries from a simple directory structure
- Automatically fit thumbnails with different dimensions into a logical grid

## Installation

```
git clone https://github.com/asmartin/f2.8gallery.git
cd f2.8gallery
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Building Your Site

First, create a directory to hold your galleries. Inside this directory, create a directory for each gallery. The name of the gallery directory should be in the format `<order>_<name>` (no spaces allowed in the directory name), for example:

```
galleries/
           1_landscapes/
           2_portraits/
           3_street_photography/
```

This will create 3 galleries with the following titles, displayed in this order:

- Landscapes
- Portraits
- Street Photography

Now, place your original, full-size JPGs in each of these directories. Then, create `about.html` and `contact.html` as needed in the same directory as `f2.8gallery.py` (see `about.example.html` and `contact.example.html` for reference).

Once you're ready, build your site:

```
source env/bin/activate
./f2.8gallery.py --title "John Smith Photos" --author "John Smith" /path/to/galleries /path/to/output
```

After your site is built, you can serve it locally to review before publishing online:

```
python3 -m http.server --directory /path/to/output
```

Now visit http://localhost:8000 to view your site. When you're ready to publish, simply sync `/path/to/output` to your hosting platform.

## Libraries

f2.8gallery is built with the following open-source technologies:

- [Inverse Icon Theme](https://github.com/yeyushengfan258/Inverse-icon-theme)
- [jQuery](https://jquery.com/)
- [jQuery Modal](https://www.jquerymodal.com/)
- [nanogallery2](https://nanogallery2.nanostudio.org/)
- [pure css](https://purecss.io/)
