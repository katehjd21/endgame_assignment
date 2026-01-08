describe('Landing page', () => {
  it('has a page title and a heading', () => {
    cy.visit('/')
    cy.title().should('eq', 'Apprenticeship Coins')
    cy.contains('h1', 'Apprenticeship Coins')
  })

  it('displays a list of all the coins', () => {
    cy.visit('/')
    cy.contains('li', 'Automate')
    cy.contains('li', 'Houston')
    cy.contains('li', 'Security')
    cy.contains('li', 'GoingDeeper')
    cy.contains('li', 'Assemble')
  })

  it('displays the automate coin as a link that navigates to the automate duties page when clicked',() => {
    cy.visit('/')
    cy.contains('a', 'Automate').click()
    cy.url().should('include', '/automate')
    cy.contains('h1', 'Automate Duties')
  })
})