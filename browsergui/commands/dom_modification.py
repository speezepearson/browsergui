from . import j, jquery_method_call

def insert_element(element):
  html = j(element.html)
  if element.previous_sibling is None:
    return jquery_method_call(element.parent, "prepend", html)
  return jquery_method_call(element.previous_sibling, "after", html)

def remove_element(element):
  html = j(element.html)
  if element.previous_sibling is None:
    return jquery_method_call(element.parent, "prepend", html)
  return jquery_method_call(element.previous_sibling, "after", html)
