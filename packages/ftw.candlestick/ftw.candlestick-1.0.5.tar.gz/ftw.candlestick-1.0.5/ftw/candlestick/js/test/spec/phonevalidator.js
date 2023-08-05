import { parse, createPhoneLink, matchPhoneGroups } from "phonevalidator";
import { phonenumbers } from "../fixtures/phonenumbers";
import { replaceTextNodesUnder } from "DOMParser";
require('babelify-es6-polyfill');
const _ = require("underscore");
const phoneUtil = require('google-libphonenumber').PhoneNumberUtil.getInstance();
const PhoneNumberFormat = require('google-libphonenumber').PhoneNumberFormat;

function decodeUnicode(str) {
  var r = /\\u([\d\w]{4})/gi;
  str = str.replace(r, function (match, grp) {
      return String.fromCharCode(parseInt(grp, 16)); } );
  return unescape(str);
}

beforeAll(() => { fixture.setBase("ftw/candlestick/js/test/fixtures"); });

afterEach(() => { fixture.cleanup(); });

describe("Phonevalidator", () => {

  describe("parse", () => {
    it("should throw an error when phonenumber is not parseable", () => {
      assert.throws(
        () => { parse("not a phonenumber") },
        Error,
        "The string supplied did not seem to be a phone number"
      );
    });

    it("should be able to parse a valid phone number", () => {
      assert.equal(
        phoneUtil.format(parse("0774561846"), PhoneNumberFormat.E164),
        "+41774561846"
      )
    });
  });

  describe("replace", () => {
    it("should create a telephone link including E164 number format", () => {
      const phoneLink = createPhoneLink("033 823 46 98");
      assert.equal(decodeUnicode(phoneLink.href), "tel:+41338234698");
      assert.equal(phoneLink.textContent, "033 823 46 98");
    });

    it("should replace all phone numbers with a phone link", () => {
      fixture.load("simple_numbers.html");
      replaceTextNodesUnder(fixture.el, createPhoneLink);
      assert.deepEqual(
        Array.from(fixture.el.querySelectorAll("a")).map((node) => {
          return { link: decodeUnicode(node.href), text: node.textContent }
        }),
        [{ link: "tel:+41417283311", text: "+41 41 728 33 11" },
         { link: "tel:+41417283701", text: "+41 41 728 37 01" }]
      )
    });
  });

  describe("matchPhoneGroup", () => {
    it("should be able to extract several phone numbers out of a string", () => {
      const possiblePhoneNumbers = `
        Peter ist auf dem Handy (076 986 78 25) erreichbar.
        Oder auch zu Hause unter + 41 (0)33 976 92 09 aber nur vom 08:00 morgens.
      `;

      assert.deepEqual(
        matchPhoneGroups(possiblePhoneNumbers),
        ["076 986 78 25", "+ 41 (0)33 976 92 09"]
      )
    });
  });
});
