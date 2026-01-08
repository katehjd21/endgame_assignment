describe('Edit Duty Feature', () => {

  beforeEach(() => {
    cy.request('POST', '/reset_duties')
    })
    
  it('can add and edit a duty', () => {
    cy.visit('/automate');

    cy.get('input[name="number"]').type(1)
    cy.get('input[name="description"]').type('Original Duty')
    cy.get('input[name="ksbs"]').type('Knowledge, Skills, Behaviours')

    cy.get('.add-duty-button').click()

    cy.contains('td', '1')
    cy.contains('td', 'Original Duty')

    cy.contains('tr', '1').within(() => {
        cy.contains('button', 'Edit').click();
    });
    cy.get('input[name="description"]').clear().type('Updated Duty');
    cy.get('input[name="ksbs"]').clear().type('K1, S1, B1');
    cy.get('button[type="submit"]').click();

    cy.contains('td', 'Updated Duty')
    cy.contains('td', 'K1, S1, B1')
  }); 
});

  