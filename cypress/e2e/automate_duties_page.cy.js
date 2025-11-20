describe('Automate Duties Page', () => {

    beforeEach(() => {
        cy.request('POST', '/reset_duties')
    }) 


    it('has a page title and heading', () => {
        cy.visit('/automate')
        cy.title().should('eq', 'Automate Duties')
        cy.contains('h1', 'Automate Duties')
    })


    it('displays a table with the headers: Duty, Description, KSBS, & Status', () => {
        cy.visit('/automate')
        cy.contains('th', 'Duty')
        cy.contains('th', 'Description')
        cy.contains('th', 'KSBS')
        cy.contains('th', 'Status')
    })


    it('allows the user to add a new duty and displays this in the Automate Duties table', () => {
        cy.visit('/automate')
        cy.get('input[name="number"]').type(1)
        cy.get('input[name="description"]').type('Test Description')
        cy.get('input[name="ksbs"]').type('Knowledge, Skills, Behaviours')

        cy.get('button[type="submit"]').click()

        cy.contains('td', '1')
        cy.contains('td', 'Test Description')
        cy.contains('td', 'Knowledge')
        cy.contains('td', 'Skills')
        cy.contains('td', 'Behaviours')
    })


    it('new duties default to not complete', () => {
        cy.visit('/automate')

        cy.get('input[name="number"]').type('2')
        cy.get('input[name="description"]').type('Another Description')
        cy.get('input[name="ksbs"]').type('Knowledge, Skills, Behaviours')

        cy.get('button[type="submit"]').click()

        cy.contains('"Duty Not Complete"')
    })


    it('splits KSBS input and renders them correctly with a comma', () => {
    cy.visit('/automate')

    cy.get('input[name="number"]').type('4')
    cy.get('input[name="description"]').type('KSBS Test')
    cy.get('input[name="ksbs"]').type('K, S, B')

    cy.get('button[type="submit"]').click()

    cy.contains('td', 'K, S, B')
    })


    it('marks a duty as complete', () => {
    cy.visit('/automate')

    cy.get('input[name="number"]').type(1)
    cy.get('input[name="description"]').type('Completed Duty Descriptio ')
    cy.get('input[name="ksbs"]').type('K, S, B')
    cy.get('button[type="submit"]').click()

    cy.contains('Complete').click()

    cy.contains('"Duty Complete!"')
    })


    it('shows multiple duties when more than one is added', () => {
        cy.visit('/automate')

        const duties = [
            { number: 1, description: 'Duty 1 Description', ksbs: 'K1, S1, B1' },
            { number: 2, description: 'Duty 2 Description', ksbs: 'K2, S2, B2' },
            { number: 3, description: 'Duty 3 Description', ksbs: 'K3, S3, B3' },
        ]

        duties.forEach(duty => {
            cy.get('input[name="number"]').type(duty.number)
            cy.get('input[name="description"]').type(duty.description)
            cy.get('input[name="ksbs"]').type(duty.ksbs)
            cy.get('button[type="submit"]').click()
        })

        cy.get('tbody tr').should('have.length', 3)
    })


    it('does not allow duplicate duty numbers', () => {
        cy.visit('/automate')

        cy.get('input[name="number"]').type(1)
        cy.get('input[name="description"]').type('Test Description 1')
        cy.get('input[name="ksbs"]').type('K, S, B')
        cy.get('button[type="submit"]').click()

        cy.get('input[name="number"]').type(1)
        cy.get('input[name="description"]').type('Test Description 2')
        cy.get('input[name="ksbs"]').type('K, S, B')
        cy.get('button[type="submit"]').click()

        cy.get('tbody tr').should('have.length', 1)
    })

    it('redirects back to /automate after user submits add duty form', () => {
    cy.visit('/automate')

    cy.get('input[name="number"]').type(1)
    cy.get('input[name="description"]').type('Test Description')
    cy.get('input[name="ksbs"]').type('K, S, B')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/automate')
})
})