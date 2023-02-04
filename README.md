# Flask_Bootstrap_Sass
Quick Start Template for Flask + Bootstrap + Sass + WTForms.

## Setup
```
pip install -r requirements.txt
npm i
flask run
```

## Customization
Some premade themes are already available in the [themes](https://github.com/Saptak625/Flask_Bootstrap_Sass_WTForms/tree/main/static/css/themes) folder. Simply change the line below in the main.scss file to the theme you would like to use. This will be autocompiled when the flask app is served.
https://github.com/Saptak625/Flask_Bootstrap_Sass_WTForms/blob/24158ea50ee68b43a7183fe08886ca88dff8a9d3/static/css/main.scss#L7-L8

### Add your own themes!
You can add your own color theme to this template by creating a theme sass file as shown below. Then, simply import your new theme into the main.scss.
https://github.com/Saptak625/Flask_Bootstrap_Sass_WTForms/blob/24158ea50ee68b43a7183fe08886ca88dff8a9d3/static/css/themes/electric_blue.scss#L1-L7
