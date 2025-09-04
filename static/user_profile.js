
$(document).ready(function() {
    // 이 html이 로드되면 뭘 할지 
    make_profile_page()
});

// 정보 요청 다 하는 큰 틀에서의 함수 (JWT 기반 현재 사용자)
function make_profile_page() {
    $.ajax({
        type: "GET",
        url: `/user/api/me`,
        success: function (response) {
            if (response['result'] === 'success') {
                display_myinfo(response);
                display_solver_info(response);
                display_my_solved_targets_info(response);
            } else {
                alert(response.msg || '로그인이 필요합니다.');
                window.location.href = '/auth/login';
            }
        },
        error: function () {
            alert('서버와 통신 중 오류가 발생했습니다.');
        }
    });
}

// 나의 정보 요청하는 함수 (보완된 버전)
function display_myinfo(user) {
    // ▼▼▼ [보완] 프로필 사진 URL 처리 로직 강화 ▼▼▼
    let profilePhotoUrl;
    const defaultPhoto = '/static/images/default_profile.png'; // 기본 이미지 경로

    // user.profilePhoto 값이 존재하는지 먼저 확인
    if (user.profilePhoto) {
        const path = user.profilePhoto;

        // 1. 절대 경로(http/https로 시작)이면 그대로 사용
        // 2. 루트 상대 경로(/로 시작)이면 그대로 사용
        // 3. 둘 다 아니면(예: 'static/uploads/...'), 앞에 '/'를 붙여 루트 상대 경로로 만들어줌
        profilePhotoUrl = /^https?:\/\//.test(path) ? path : (path.startsWith('/') ? path : `/${path}`);
    } else {
        // 프로필 사진 정보가 없으면 기본 이미지 사용
        profilePhotoUrl = defaultPhoto;
    }

    // onerror 이벤트를 추가하여 URL이 잘못되었을 경우에도 기본 이미지로 대체
    $('#profile-img')
        .attr('src', profilePhotoUrl)
        .on('error', function() {
            $(this).attr('src', defaultPhoto);
        });
    // ▲▲▲ [보완] 프로필 사진 설정 완료 ▲▲▲


    const my_info_html = `
        <li class="flex justify-between"><strong>닉네임:</strong> <span>${user.nickName}</span></li>
        <li class="flex justify-between"><strong>MBTI:</strong> <span>${user.mbti}</span></li>
        <li class="flex justify-between"><strong>취미:</strong> <span>${user.hobby}</span></li>
        <li class="flex justify-between"><strong>좋아하는 음식:</strong> <span>${user.favoriteFood}</span></li>
        <li class="mt-2 pt-2 border-t"><strong>한 줄 소개:</strong><p class="text-sm text-gray-600">${user.selfIntro}</p></li>
        <li class="mt-2 pt-2 border-t"><strong>지원 동기:</strong><p class="text-sm text-gray-600">${user.selfMotive}</p></li>
    `;
    $('#my-profile').html(my_info_html);
}


// '나를 맞춘 사람' 섹션을 채우는 함수
function display_solver_info(user) {
    $('#my-solver').empty(); // 기존 내용을 비웁니다.
    if (user.userWhoSolvedMeCount === 0) {
        $('#my-solver').html(`<p class="text-gray-500">아직 나를 맞춘 사람이 없어요.</p>`);
    } else {
        // [수정] userWhoSolvedMe는 ID가 담긴 '배열'이므로, 각 ID에 대해 카드를 만듭니다.
        makeUserCard(user.userWhoSolvedMe, "#my-solver");
    }
}

// '내가 맞춘 사람' 섹션을 채우는 함수
function display_my_solved_targets_info(user) {
    $('#my-solved-list').empty(); // 기존 내용을 비웁니다.
    if (user.usersISolvedCount === 0) {
        $('#my-solved-list').html(`<p class="text-gray-500">아직 내가 맞춘 사람이 없어요.</p>`);
    } else {
        // [수정] usersISolved도 '배열'이므로, 각 ID에 대해 카드를 만듭니다.
        user.usersISolved.forEach(solvedUserId => {
            makeUserCard(solvedUserId, '#my-solved-list');
        });
    }
}

// [개선] 사용자 ID와 카드를 추가할 HTML 영역을 받아,
// API 요청 후 사용자 카드를 만들어주는 공통 함수
function makeUserCard(userId, targetElementSelector) {
    $.ajax({
        type: "GET",
        url: `/user/api/users/${userId}`, // Blueprint 접두사 '/user' 포함
        success: function (response) {
            if (response.result === 'success') {
                const card_html = `
                <div class="border rounded-lg p-3 my-2 shadow-sm bg-gray-50">
                    <p class="font-semibold text-green-800">${response.userName} (${response.nickName})</p>
                    <p class="text-sm text-gray-600 mt-1">${response.selfIntro}</p>
                </div>
                `;
                $(targetElementSelector).append(card_html);
            }
        },
        error: function() {
            console.error(`ID가 ${userId}인 사용자 정보를 가져오는 데 실패했습니다.`);
        }
    });
}