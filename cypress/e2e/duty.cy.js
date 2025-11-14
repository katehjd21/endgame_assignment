describe('Display a Single Duty with the relevant information', () => {
  it('It displays a single Duty', () => {
    cy.visit('/')
    cy.contains('h1', 'Duty 1')
    cy.contains('p', 'Random Duty Description')
    cy.contains('li', 'Knowledge')
    cy.contains('li', 'Skills')
    cy.contains('li', 'Behaviours')
    cy.contains('p', 'Duty Not Completed!')
  })
})

