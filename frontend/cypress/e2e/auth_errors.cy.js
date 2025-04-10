describe('Auth Errors', () => {
    it('Shows error when fields are empty on register', () => {
      cy.visit('/');
      cy.get('.v-tab').contains('Register').click();
      cy.get('[data-cy="register-submit"]').click();
      cy.contains('Please fill in all fields');
    });
  
    it('Shows error when passwords do not match', () => {
      cy.visit('/');
      cy.get('.v-tab').contains('Register').click();
      cy.get('[data-cy="register-username"]').type('TestUser');
      cy.get('[data-cy="register-email"]').type('testuser@example.com');
      cy.get('[data-cy="register-password"]').type('password123');
      cy.get('[data-cy="register-confirm"]').type('differentPass');
      cy.get('[data-cy="register-submit"]').click();
      cy.contains('Passwords do not match');
    });
  
    it('Shows error when logging in with wrong credentials', () => {
      cy.visit('/');
      cy.get('.v-tab').contains('Login').click();
      cy.get('[data-cy="login-email"]').type('wrong@example.com');
      cy.get('[data-cy="login-password"]').type('wrongpassword');
      cy.get('[data-cy="login-submit"]').click();
      cy.get('[data-cy="auth-error"]').should('contain', 'Invalid email or password.');
    });
  });
  