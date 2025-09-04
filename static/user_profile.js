
$(document).ready(function() {
    make_profile_page()
});

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

function display_myinfo(user) {
    let profilePhotoUrl;
    const defaultPhoto = '/static/images/default_profile.png'; 

    if (user.profilePhoto) {
        const path = user.profilePhoto;

        profilePhotoUrl = /^https?:\/\//.test(path) ? path : (path.startsWith('/') ? path : `/${path}`);
    } else {
        profilePhotoUrl = defaultPhoto;
    }

    $('#profile-img')
        .attr('src', profilePhotoUrl)
        .on('error', function() {
            $(this).attr('src', defaultPhoto);
        });


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


function display_solver_info(user) {
    $('#my-solver').empty(); 
    if (user.userWhoSolvedMeCount === 0) {
        $('#my-solver').html(`<p class="text-gray-500">아직 나를 맞춘 사람이 없어요.</p>`);
    } else {
        makeUserCard(user.userWhoSolvedMe, "#my-solver");
    }
}

function display_my_solved_targets_info(user) {
    $('#my-solved-list').empty();
    if (user.usersISolvedCount === 0) {
        $('#my-solved-list').html(`<p class="text-gray-500">아직 내가 맞춘 사람이 없어요.</p>`);
    } else {
        user.usersISolved.forEach(solvedUserId => {
            makeUserCard(solvedUserId, '#my-solved-list');
        });
    }
}

function makeUserCard(userId, targetElementSelector) {
    $.ajax({
        type: "GET",
        url: `/user/api/users/${userId}`, 
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