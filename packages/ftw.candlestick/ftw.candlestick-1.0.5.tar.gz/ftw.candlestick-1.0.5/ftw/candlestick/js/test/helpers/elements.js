// These helpers generate text nodes as they would be generated from the treeWalter
// in the DOMParser

export function createElement(type="span", text="033 723 50 80") {
  var element = document.createElement(type);
  element.textContent = text;
  return (element.childNodes || element.childNodes[0]) && element;
}

export function createInput(type="text", value="033 723 50 80") {
  var input = createElement("input");
  input.type = type;
  input.value = value;
  return input.childNodes[0];
}

export function createLink(href="#", text="033 723 50 80") {
  var link = createElement("a");
  link.href = href;
  link.textContent = text;
  return link.childNodes[0];
}
