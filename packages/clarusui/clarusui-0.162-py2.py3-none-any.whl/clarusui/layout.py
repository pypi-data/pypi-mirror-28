from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from abc import ABCMeta, abstractmethod
import clarusui.colours
import webbrowser

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(THIS_DIR),
    #loader=FileSystemLoader('/templates/'),
    autoescape=select_autoescape(['html', 'xml'])
)

layout_template = env.get_template('layout.html')
header_template = env.get_template('header.html')
            
class Element(object):
    
    __metaclass__ = ABCMeta
    def __init__(self, response, **options):
        self.response = response
        self.set_css_class(options.pop('cssClass', ''))
        self.set_size(options.pop('size', None))
        self.customCss = {}
        self.set_custom_css(options.pop('customCss', None))
        self.set_height(options.pop('height', None))
        if options.get('bgcolour') is not None:
            self.add_custom_css({'background-color':options.get('bgcolour')})
        self.options = dict(options)
        self.set_header(options.pop('header',''))
        
                   
    def _get_rgbcolour(self, colour):
#         if colour is None:
#             return None;
#         if colour.startswith('#'):
#             return colour        
#         if colour.startswith('RGB'):
#             return colour    
#         
#         return colours.rgbcolours.get(colour)
        return colour
    
    def __str__(self):
        return self.toHTML()

    @abstractmethod
    def toDiv(self):
        pass

    def toFile(self):
        tempFileName = 'temp-element.html'
        with open(tempFileName, 'w') as f:
            f.write(self.toHTML())
                    
        url = 'file://' + os.path.abspath(tempFileName)
        webbrowser.open(url)
        return url
            
  
    def toHTML(self):
        self.add_custom_css({'min-height':'100vh'}) #should be the final step so should at least fill viewpoet
        base = env.get_template('base_content.html')
        return base.render(content=self.toDiv())
   
    def toCSV(self):
        return self.response.text
        
    def set_css_class(self, cssClass):
        if (cssClass is not None):
            self.cssClass = cssClass
        else:
            self.cssClass = ''
            
    def set_custom_css(self, customCss):
        if (customCss is not None):
            self.customCss = customCss
    
    def add_custom_css(self, customCss):
        for key in customCss:
            self.customCss[key] = customCss.get(key)
            
    def _get_custom_css(self):
        if not self.customCss:
            return ''
        else:
            css = 'style="'
            for key in self.customCss:
                css = css + key + ':' + self.customCss.get(key) + ';'
            css = css + '"' 
            return css

    def set_bgcolour(self, colour):
        if colour is not None:
            self.add_custom_css({'background-color':colour})

    def set_size(self, size):
        if size is not None:
            if not isinstance(size, int):
                raise TypeError("size must be an integer")
            if size > 12 or size < 1:
                raise ValueError("size must be 1 <= x <= 12 when specified")
        self.size = size
        
    def set_height(self, height):
        if height is not None:
            self.add_custom_css({'overflow-y':'auto', 'max-height':height})
    
    def _cascade_style(self, style):
        if 'background-color' not in self.customCss:
            self.set_bgcolour(style.getForegroundColour())
        self.set_font(style)
    
    def set_font(self, style):
        if style is not None:
            if 'color' not in self.customCss:
                self.add_custom_css({"color":style.getFontColour()})
            if 'font-family' not in self.customCss:
                self.add_custom_css({'font-family':style.getFontFamily()})
    
    def set_header(self, header):
        self._header = header
        
    def _get_header(self):
        return self._header
            
        
        

class Dashboard(Element):
    def __init__(self, *childElements, **options):
        super(Dashboard, self).__init__(None,**options)
        #self.childElements = childElements
        self.displayHeader = options.pop('displayHeader', bool(self._get_header()))
        self._set_child_elements(childElements)
        self.uniformColumnSize = options.pop('uniformColumnSize', False)
        self._finalise_column_sizing()
        #self.add_custom_css({'padding-top':'0.9375rem'})
        #self.add_custom_css({'padding-bottom':'0.9375rem'})
        
        style = options.pop('style', None)
        if style is not None:
            self._set_style(style)
        
    
    def _set_style(self, style):
        self.set_bgcolour(style.getBackgroundColour())
        if self.displayHeader == True:
            self._header_element.set_bgcolour(style.getBackgroundColour())
        for elements in self.childElements:
            for element in elements:
                element._cascade_style(style)
        
        
     
    def _set_child_elements(self, childElements):
        self.childElements = []
        
        if self.displayHeader == True:
            self.childElements.append([self._create_header_element()])
        
        for element in childElements:
            if not isinstance(element, list):
                self.childElements.append([element])
            else:
                self.childElements.append(element)
        
    def _finalise_column_sizing(self):
        if self.uniformColumnSize == True:
            self._uniform_column_size()
        else:
            self._auto_column_size()
        
    def _auto_column_size(self):
        for elements in self.childElements:
            holder = []
            unsizedElementCount = 0
            unpecifiedSizeRemaining = 12
    
            for element in elements:
                if element.size is None:
                    unsizedElementCount += 1
                else:
                    unpecifiedSizeRemaining = unpecifiedSizeRemaining - element.size
                holder.append(element)
            if unpecifiedSizeRemaining < 0:
                raise ValueError("specified sizes must total to <= 12")
    
            if (unsizedElementCount > 0):
                unspecifiedElementSize = int(unpecifiedSizeRemaining/unsizedElementCount)
                for i in holder:
                    if i.size is None:
                        i.size = unspecifiedElementSize
    
    def _uniform_column_size(self):
        maxNoOfColumns = 1
        for elements in self.childElements:
            if len(elements) > maxNoOfColumns:
                maxNoOfColumns = len(elements)
                
        for elements in self.childElements:
            for element in elements:
                element.size = int(12/maxNoOfColumns)
    
    def _create_header_element(self):
        header = Header(header=self._get_header())
        header.add_custom_css({'border-bottom-style':'solid', 'border-bottom-width':'1px'})
        self._header_element = header
        return self._header_element
               
    def toDiv(self):
        return layout_template.render(dashboard=self)
    
class Grid(Dashboard):
    def __init__(self, *childElements, **options):
        self.columns = options.pop('columns', 2)
        laidOutChildren = self._layout_children(*childElements)
        super(self.__class__, self).__init__(uniformColumnSize=True,*laidOutChildren,**options)
        
    def _layout_children(self, childElements):
        chunks = self._chunk(childElements, self.columns)
        return list(chunks)
    
    def _chunk(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]  
            
class Header(Element):
    def __init__(self, **options):
        super(self.__class__, self).__init__(None, **options)      
    
    def toDiv(self):
        return header_template.render(header=self)