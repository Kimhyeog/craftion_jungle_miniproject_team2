document.addEventListener('DOMContentLoaded', function() {
  
    // 모든 유저 카드에 클릭 이벤트 추가
    const userCards = document.querySelectorAll('.user-card');
    userCards.forEach(card => {
      card.addEventListener('click', function() {
        const userId = this.getAttribute('data-user-id');
        // 특정 유저의 상세 페이지로 이동
        window.location.href = `/user/profile/${userId}`;
      });
    });
    
    // 실시간 검색 기능
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', function() {
        const keyword = this.value.toLowerCase().trim();
        filterCards(keyword);
      });
    }
  });
  
  /**
   * 키워드를 기반으로 유저 카드를 필터링하는 함수
   * @param {string} keyword - 검색어
   */
  function filterCards(keyword) {
    const cards = document.querySelectorAll('.user-card');
    let visibleCount = 0;
    
    cards.forEach(card => {
      // data-search 속성을 가진 모든 요소들 찾기
      const searchableElements = card.querySelectorAll('[data-search]');
      let searchableText = '';
      
      // 각 검색 가능한 요소의 텍스트를 수집
      searchableElements.forEach(element => {
        searchableText += element.textContent.toLowerCase() + ' ';
      });
      
      // 검색어가 비어있거나 포함되어 있으면 표시
      if (keyword === '' || searchableText.includes(keyword)) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });
    
    // 검색 결과가 없을 때 메시지 표시
    updateNoResultsMessage(keyword, visibleCount);
  }
  
  /**
   * '검색 결과 없음' 메시지를 업데이트하는 함수
   * @param {string} keyword - 검색어
   * @param {number} visibleCount - 화면에 보이는 카드 수
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