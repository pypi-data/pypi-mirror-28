import { parse,
         extractTextNodesUnder,
         replaceTextNodesUnder,
         acceptNodeFilter,
         extractNodes,
         replaceTextNodes,
         splitTextNode
       } from "DOMParser";

import { createElement,
         createInput,
         createLink
       } from "../helpers/elements";

beforeAll(() => { fixture.setBase("ftw/candlestick/js/test/fixtures"); });

afterEach(() => { fixture.cleanup(); });

describe("DOMParser", () => {

  chai.config.truncateThreshold = 0;

  describe("acceptFilter", () => {
    it("should not accept empty text nodes", () => {
      const emptyNode = createElement("span", "");
      assert.equal(acceptNodeFilter(emptyNode), NodeFilter.FILTER_REJECT);
    });

    it("should not accept text node including text", () => {
      const invalidPhoneNode = createElement("span", "this is not a valid phone number");
      assert.equal(acceptNodeFilter(invalidPhoneNode), NodeFilter.FILTER_REJECT);
    });

    it("should not accept text node including impossible number", () => {
      const invalidPhoneNode = createElement("span", "21");
      assert.equal(acceptNodeFilter(invalidPhoneNode), NodeFilter.FILTER_REJECT);
    });

    it("should accept text node with valid phone number", () => {
      const phoneNumber = createElement();
      assert.equal(acceptNodeFilter(phoneNumber), NodeFilter.FILTER_ACCEPT);
    });

    it("should not accept input fields", () => {
      const inputField = createInput();
      assert.equal(acceptNodeFilter(inputField), NodeFilter.FILTER_REJECT);
    });

    it("should not accept links", () => {
      const link = createLink();
      assert.equal(acceptNodeFilter(link), NodeFilter.FILTER_REJECT);
    });

    it("should not accept textareas", () => {
      const textarea = createElement("textarea");
      assert.equal(acceptNodeFilter(textarea), NodeFilter.FILTER_REJECT);
    });

    it("should accept containers", () => {
      const container = createElement("div");
      assert.equal(acceptNodeFilter(container), NodeFilter.FILTER_ACCEPT);
    });
  });

  describe("extract", () => {

    it("should extract all text nodes from html source", () => {
      fixture.load("text_nodes.html");
      const treeWalker = document.createTreeWalker(fixture.el, NodeFilter.SHOW_TEXT, null, false);
      assert.deepEqual(
        extractNodes(treeWalker).map(node => node.textContent),
        ["1", "2", "3", "4", "5"]
      );
    });

    it("should extract all text nodes from html source", () => {
      fixture.load("simple_numbers.html");
      assert.deepEqual(
        extractTextNodesUnder(fixture.el).map(node => node.textContent),
        ["Tel. +41 41 728 33 11", "Fax +41 41 728 37 01"]
      );
    });
  });

  describe("replace", () => {
    it("should throw an error if the new nodes does not match the substrings", () => {
      assert.throw(() => {
        replaceTextNodes("test", [1], []);
      }, Error, "The nodes to replace does not match the substrings")
    });

    it("should replace a part in a text node", () => {
      fixture.load("simple_numbers.html");
      const node = createElement("span", "this is to replace {1} {2}");
      const newNode = createElement("span", "replaced");
      replaceTextNodes(node.childNodes[0], ["{1}", "{2}"], [newNode, newNode]);
      assert.equal(node.outerHTML,
        "<span>this is to replace <span>replaced</span> <span>replaced</span></span>"
      );
    });

    it("should be able to replace multiple parts in a text node", () => {
      fixture.load("complex_numbers.html");
      const textNode = fixture.el.querySelector("p").childNodes[0];
      const newNode = createElement("span", "replaced");
      replaceTextNodes(
        textNode,
        ["(076 986 78 25)", "+ 41 (0)33 976 92 09"],
        [newNode, newNode]
      );
      assert.equal(fixture.el.querySelector("p").outerHTML,
        '<p>Handy: <span>replaced</span> erreichbar oder privat <span>replaced</span></p>'
      );
    });

    it("should replace multiple parts in a text node", () => {
      fixture.load("complex_numbers.html");
      const textNode = fixture.el.querySelector("p").childNodes[0];
      replaceTextNodesUnder(fixture.el);
      assert.equal(fixture.el.querySelector("p").outerHTML,
        '<p>Handy: (<a href="tel:+41769867825">076 986 78 25</a>) erreichbar oder privat <a href="tel:+41339769209">+ 41 (0)33 976 92 09</a></p>'
      );
    });

    it("should replace phone numbers with phone links", () => {
      fixture.load("simple_numbers.html");
      replaceTextNodesUnder(fixture.el);
      assert.deepEqual(
        Array.from(fixture.el.querySelectorAll("a")).map(node => {
          return { text: node.textContent, link: node.href }
        }),
        [{ text: "+41 41 728 33 11", link: "tel:+41417283311" },
         { text: "+41 41 728 37 01", link: "tel:+41417283701" }]
      );
    });
  });

});
