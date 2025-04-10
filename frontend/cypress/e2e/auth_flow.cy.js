describe('Auth Flow - Register, Logout, Login', () => {
    const timestamp = Date.now();
    const email = `user${timestamp}@test.com`;
    const password = 'password123';
    const username = `user${timestamp}`;
  
    it('Registers, logs out, and logs back in', () => {
      cy.visit('/');
  
      cy.get('.v-tab').contains('Register').click();
      cy.get('[data-cy="register-username"]').type(username);
      cy.get('[data-cy="register-email"]').type(email);
      cy.get('[data-cy="register-password"]').type(password);
      cy.get('[data-cy="register-confirm"]').type(password);
      cy.get('[data-cy="register-submit"]').click();
  
      cy.contains('Dashboard', { timeout: 10000 });
  
      cy.get('[data-cy="logout-btn"]').click();
      cy.url().should('include', '/');
  
      cy.get('.v-tab').contains('Login').click();
      cy.get('[data-cy="login-email"]').type(email);
      cy.get('[data-cy="login-password"]').type(password);
      cy.get('[data-cy="login-submit"]').click();
  
      cy.contains('Dashboard', { timeout: 10000 });
    });
  });
  