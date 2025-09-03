function  showModal(title, message) 
{
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modal-title");
  const modalMessage = document.getElementById("modal-message");
  const closeBtn = document.getElementById("close-modal");

  modalTitle.textContent = title;
  modalMessage.innerHTML = message;

  modal.classList.remove("hidden");

  closeBtn.onclick = () => {
    modal.classList.add("hidden");
  };

}

document.addEventListener('DOMContentLoaded', async () => {
    // 1) 내 정보 불러와서 프리필
    try {
      const meRes = await fetch('/user/api/me');
      if (!meRes.ok) throw new Error('unauthorized');
      const me = await meRes.json();
      if (me.result !== 'success') throw new Error(me.msg || 'fail');
      const f = document.getElementById('profile-edit-form');
      f.nickName.value = me.nickName || '';
      f.hobby.value = me.hobby || '';
      f.mbti.value = me.mbti || '';
      f.oneLineIntro.value = me.selfIntro || '';
      f.motivate.value = me.selfMotive || '';
      f.favoriteFood.value = me.favoriteFood || '';
    } catch (e) {
      alert('로그인이 필요합니다.');
      location.href = '/auth/login';
      return;
    }
  
    // 2) 제출 처리
    const form = document.getElementById('profile-edit-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const res = await fetch(form.action, { method: 'POST', body: formData });
      const data = await res.json();
      if (data.result === 'success') {
        showModal("수정 완료", "수정이 완료되었습니다.<br>메인 페이지로 이동합니다");
        setTimeout(() => {
          window.location.href = '/quiz/list';
        }, 2000)
      } else {
        showModal("에러", data.msg || '수정 중 오류가 발생했습니다.');
      }
    });
  });