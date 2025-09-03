
$(document).ready(function() {
    // 이 html이 로드되면 뭘 할지 
    make_profile_page()
});

// 정보 요청 다 하는 큰 틀에서의 함수
function    make_profile_page() {
// [수정] 하드코딩된 ID 대신, HTML의 data-userid 속성에서 ID를 가져옵니다.
    // 1. HTML에서 사용자 ID를 가져온다.    
    const userId = '1'; //userId는 JWT 토큰에서 가져온다 

    // 2. 만약 ID가 없다면?
    if (!db_id) {
       // 여기서 함수가 중단(return)되어 버린다!
        alert("사용자 정보를 불러올 수 없습니다. URL에 ID가 포함되어 있는지 확인하세요.");
        return;
    }

    $.ajax({
        type: "GET",
        // [수정] url 주소 앞에 '/user'를 추가합니다.
        url: `/user/api/users/${userId}`, // [수정] /user 접두사 추가,
        success: function (response) {
            if (response['result'] == 'success') {
                
                // 성공 시, 각 섹션에 정보를 채워넣는 함수들을 호출합니다.
                display_myinfo(response);
                display_solver_info(response);
                display_my_solved_targets_info(response);
            }
            error: ()=>alert("서버와 통신 중 오류가 발생했습니다.");
        
        }
    });

}

// 나의 정보 요청하는 함수 
function display_myinfo(user) {
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
        user.userWhoSolvedMe.forEach(solverId => {
            makeUserCard(solverId, '#my-solver');
        });
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