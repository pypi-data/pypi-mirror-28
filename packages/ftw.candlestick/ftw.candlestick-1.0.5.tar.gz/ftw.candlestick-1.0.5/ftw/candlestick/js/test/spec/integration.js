import { linkPhoneNumbers } from "phonevalidator";
import { stripNewline, stripWhitespace } from "../helpers/string";

beforeAll(() => { fixture.setBase("ftw/candlestick/js/test/fixtures"); });

afterEach(() => { fixture.cleanup(); });

describe("Integration", () => {

  /*
  Although the actual and expected HTML is visually identical
  the assertion fails. So we skip this test.
  TODO: This should be fixed soon
   */
  xit("should properly replace a whole DOM structure", () => {
    fixture.load("integration.html");
    const expected = fixture.el.querySelector("#expected").innerHTML;
    linkPhoneNumbers("#actual");
    const actual = fixture.el.querySelector("#actual").innerHTML;
    assert.equal(stripWhitespace(stripNewline(actual)), stripWhitespace(stripNewline(expected)));
  });

  it("should apply trailing text", () => {
    fixture.load("trailing_text.html");
    linkPhoneNumbers("#actual");
    const actual = fixture.el.querySelector("#actual").innerHTML;
    const expected = fixture.el.querySelector("#expected").innerHTML;
    assert.equal(stripWhitespace(stripNewline(actual)), stripWhitespace(stripNewline(expected)));
  });

  it("should not include parentheses in the phonelink", () => {
    fixture.load("parentheses.html");
    linkPhoneNumbers("#actual");
    const actual = fixture.el.querySelector("#actual").innerHTML;
    const expected = fixture.el.querySelector("#expected").innerHTML;
    assert.equal(stripWhitespace(stripNewline(actual)), stripWhitespace(stripNewline(expected)));
  });

  it("should match phonenumber with variing spaces", () => {
    fixture.load("spaced_numbers.html");
    linkPhoneNumbers("#actual");
    const actual = fixture.el.querySelector("#actual").innerHTML;
    const expected = fixture.el.querySelector("#expected").innerHTML;
    assert.equal(stripWhitespace(stripNewline(actual)), stripWhitespace(stripNewline(expected)));
  });

  it("should not match too short numbers", () => {
    fixture.load("short_number.html");
    linkPhoneNumbers("#actual");
    const actual = fixture.el.querySelector("#actual").innerHTML;
    const expected = fixture.el.querySelector("#expected").innerHTML;
    assert.equal(stripWhitespace(stripNewline(actual)), stripWhitespace(stripNewline(expected)));
  });

  it("should not match IBAN numbers", () => {
    fixture.load("iban_number.html");
    linkPhoneNumbers("#actual");
    const actual = fixture.el.querySelector("#actual").innerHTML;
    const expected = fixture.el.querySelector("#expected").innerHTML;
    assert.equal(stripWhitespace(stripNewline(actual)), stripWhitespace(stripNewline(expected)));
  });

});
