
$(document).ready(function() {
    // 이 html이 로드되면 뭘 할지 
    make_profile_page()
});

// 정보 요청 다 하는 큰 틀에서의 함수
function    make_profile_page() {

    const db_id = "68b71902c2592ccd641f586b";

    $.ajax({
        type: "GET",
        url: `/api/users/${db_id}`,
        success: function (response) {
            if (response['result'] == 'success') {
                get_myinfo(response)
                get_solver_info(response)
                get_my_solved_targets_info(response)
            }
            else
                alert ('사용자 정보 받아오기 실패')
        }
    });

}

// 나의 정보 요청하는 함수 
function    get_myinfo(response)
{
// 정보 받은거 html 요소로 넣어서 append
    const my_info = `
        <li>닉네임: ${response.nickName}</li>
        <li>자기소개: ${response.selfIntro}</li>
        <li>동기: ${response.selfMotive}</li>
        <li>좋아하는 음식: ${response.favoriteFood}</li>
        <li>취미: ${response.hobby}</li>
        <li>MBTI: ${response.mbti}</li>
    `
    $('#my-profile').html(my_info)
}


// 나를 맞춘 사람 정보 요청하는 함수
function    get_solver_info(response) 
{
    $('#my-solver').html("")
    console.log(response.userWhoSolvedMeCount)
    if (response.userWhoSolvedMeCount == 0)
    {
        const not_found_notice = `
            <h2> 문제를 푼 사람이 아직 없어요. 조금만 기다려주세요. </h2>
        `
        $('#my-solver').html(not_found_notice)
    }
    else
    {
        make_my_solver_card(response.userWhoSolvedMe)
        const my_solver_notice = `
            
        `
        $('#my-solver').html(my_solver_notice)
    }
}

function    make_my_solver_card(userDbId)
{
    $.ajax({
        type: "GET",
        url: `/api/users/${userDbId}`,
        success: function (response) {
            if (response['result'] == 'success')
            {
                let tmpCard = `
                    <h2> 문제를 맞추신 분은 ${response.userName}님입니다! 같이 식사를 하세요! </h2>
                `
                $('#my-solver').append(tmpCard)
            }
            else
            {
                alert ('내가 맞춘 사람 정보 찾기 실패')
            }
        }
    })
}

// 내가 맞춘 사람 정보 요청하는 함수 
function    get_my_solved_targets_info(response)
{
    $('#my-solved-list')
    if (response.usersISolvedCount == 0)
    {
        const   not_found_notice = `
            <h2> 내가 맞춘 사람이 아직 없어요. 분발하세요. </h2>
        `
        $('#my-solved-list').html(not_found_notice)
    }
    else
    {
        // 여기 카드 형식으로 꾸밈이 들어가야 할 듯 
        for (let i = 0; i < response.usersISolvedCount; i++)
            makeUserCard(response.usersISolved[i])
    }
}

function    makeUserCard(userDbId)
{
    $.ajax({
        type: "GET",
        url: `/api/users/${userDbId}`,
        success: function (response) {
            if (response['result'] == 'success')
            {
                let tmpCard = `
                <div>
                    <p> ${response.userName} </p>
                    <p> ${response.selfIntro} </p>
                </div>
                `
                $('#my-solved-list').append(tmpCard)
            }
            else
            {
                alert ('내가 맞춘 사람 정보 찾기 실패')
            }
        }
    })
}