import { replaceTextNodesUnder } from "./DOMParser"

const repeat = require("repeat-string");
const phoneUtil = require("google-libphonenumber").PhoneNumberUtil.getInstance();
const PhoneNumberFormat = require("google-libphonenumber").PhoneNumberFormat;

const defaultCountry = "CH"; // ISO 3166-1 two-letter country code

const possibleNumberRegEx = /(\+|0|\(0\)){1}(33)?( )*(41)?( )*(\(0\))?(\d){0,2}(41)?( )*(41)?( )*(\d){3}( )*(\d){2}( )*(\d){2}/g;

/*
  This function tries to find phone number candidates out
  of a string.
  The string may contain some phone numbers in different formats.
  These candidates are passed through the google-libphonenumber library
  to make sure we got a valid phone number.
 */
export function matchPhoneGroups(possiblePhoneNumbers) {
  return (possiblePhoneNumbers.match(possibleNumberRegEx) || [])
         .map((phoneNumber) => phoneNumber.trim());
}

export function parse(phoneNumber) { return phoneUtil.parse(phoneNumber, defaultCountry); }

export function createPhoneLink(phoneNumber) {
  const parsedNumber = parse(phoneNumber);
  if(!phoneUtil.isValidNumber(parsedNumber)) {
    return document.createTextNode(phoneNumber);
  }
  let internationalNumber = phoneUtil.format(parsedNumber, PhoneNumberFormat.E164);
  let phoneLink = document.createElement("a");
  phoneLink.href = `tel:${internationalNumber}`;
  phoneLink.textContent = phoneNumber;
  return phoneLink;
}

export function linkPhoneNumbers(root="body") {
  replaceTextNodesUnder(document.querySelector(root));
}
