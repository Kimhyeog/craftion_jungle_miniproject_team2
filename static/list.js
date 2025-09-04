document.addEventListener('DOMContentLoaded', function() {
  
    const userCards = document.querySelectorAll('.user-card');
    userCards.forEach(card => {
      card.addEventListener('click', function() {
        const userId = this.getAttribute('data-user-id');
        window.location.href = `/user/profile/${userId}`;
      });
    });
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', function() {
        const keyword = this.value.toLowerCase().trim();
        filterCards(keyword);
      });
    }
  });
  
  /**
   * 
   * @param {string} keyword 
   */
  function filterCards(keyword) {
    const cards = document.querySelectorAll('.user-card');
    let visibleCount = 0;
    
    cards.forEach(card => {
      const searchableElements = card.querySelectorAll('[data-search]');
      let searchableText = '';
      
      searchableElements.forEach(element => {
        searchableText += element.textContent.toLowerCase() + ' ';
      });
      
      if (keyword === '' || searchableText.includes(keyword)) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });
    
    updateNoResultsMessage(keyword, visibleCount);
  }
  
  /**
   * 
   * @param {string} keyword 
   * @param {number} visibleCount 
   */
  function updateNoResultsMessage(keyword, visibleCount) {
    const noResultsDiv = document.getElementById('noResults');
    
    if (keyword && visibleCount === 0) {
      noResultsDiv.style.display = 'block';
      noResultsDiv.innerHTML = `
        <div class="text-4xl mb-2">🔍</div>
        <p class="text-gray-600">"${keyword}"에 대한 검색 결과가 없습니다.</p>
      `;
    } else {
      noResultsDiv.style.display = 'none';
    }
  }