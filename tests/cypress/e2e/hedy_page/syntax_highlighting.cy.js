import { loginForUser } from "../tools/login/login";
import { goToHedyPage, goToAdventurePage } from "../tools/navigation/nav";

describe('The Hedy level 1 print adventure page', () => {
  beforeEach(() => {
    goToAdventurePage();
  });

  it('has the word print highlighted in examples', () => {
    cy.get('#adventures-tab pre')
      .contains('print')
      .should('be.visible')
      .and('have.class', 'ace_keyword');
  })
});

describe('The view program page', () => {
  let programName;
  beforeEach(async () => {
    loginForUser();
    goToHedyPage();
    programName = Math.random().toString(36);
    cy.get('#program_name').clear().type(programName);
    cy.get('#share_program_button').click();
    cy.get('#share-public').click();
    cy.get('button[data-action="copy-to-clipboard"]').click();

    const urlFromClipboard = await new Promise((ok) =>
      cy.window().then((win) =>
        win.navigator.clipboard.readText().then(ok)));

    cy.visit(urlFromClipboard);
  });
})

describe('The raw program page', () => {
  beforeEach(() => {
    cy.visit('/adventure/story/1/raw');
  });
});
