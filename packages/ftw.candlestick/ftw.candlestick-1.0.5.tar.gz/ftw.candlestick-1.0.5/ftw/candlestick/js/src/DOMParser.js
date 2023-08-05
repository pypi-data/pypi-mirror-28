import { parse, matchPhoneGroups, createPhoneLink } from "./phonevalidator";

const escapeStringRegExp = require("escape-string-regexp");
const includes = require("array-includes");

const blacklist = [
  "A",
  "INPUT",
  "TEXTAREA"
]

function isBlacklisted(node) { return includes(blacklist, node.nodeName); }

export function acceptNodeFilter(node) {
  if(node.nodeType !== Node.TEXT_NODE && isBlacklisted(node)) {
    return NodeFilter.FILTER_REJECT;
  }
  if(node.nodeType === Node.TEXT_NODE && node.parentNode && isBlacklisted(node.parentNode)) {
    return NodeFilter.FILTER_REJECT;
  }
  if(!matchPhoneGroups(node.textContent).length) {
    return NodeFilter.FILTER_REJECT;
  }
  return NodeFilter.FILTER_ACCEPT;
}

export function extractNodes(walker, nodes=[]) {
  let nextNode = walker.nextNode();
  if(!nextNode) {
    return nodes;
  } else {
    return extractNodes(walker, nodes.concat(nextNode))
  }
}

export function mergeStringToRegExp(parts, flags="") {
  return new RegExp(parts.map(escapeStringRegExp).join("|"), flags);
}

export function replaceTextNodes(textNode, subStr=[], newNodes=[]) {
  if(subStr.length !== newNodes.length) {
    throw new Error("The nodes to replace does not match the substrings");
  }
  if (textNode.parentNode) {
    const subStrRegExp = mergeStringToRegExp(subStr, "g");
    let gabs = textNode.textContent.split(subStrRegExp);
    let matches = textNode.textContent.match(subStrRegExp);
    let parentNode = textNode.parentNode;

    gabs = gabs.map(part => document.createTextNode(part));
    matches = matches.map((match, index) => newNodes[index]);

    matches.forEach((match, index) => {
      parentNode.insertBefore(gabs[index].cloneNode(true), textNode);
      parentNode.insertBefore(match.cloneNode(true), textNode);
    });

    parentNode.insertBefore(gabs[gabs.length - 1].cloneNode(true), textNode);

    parentNode.removeChild(textNode);
  }
}

export function extractTextNodesUnder(root) {
  return extractNodes(document.createNodeIterator(root, NodeFilter.SHOW_TEXT, acceptNodeFilter, false));
}

export function replaceTextNodesUnder(root) {
  let textNodes = extractTextNodesUnder(root);
  textNodes.forEach((textNode) => {
    let phoneGroups = matchPhoneGroups(textNode.textContent);
    replaceTextNodes(textNode, phoneGroups, phoneGroups.map(createPhoneLink));
  });
}
