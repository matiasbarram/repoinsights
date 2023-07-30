# Repositty
- get repos/user/repo - 1
- get users/user - 1


# commits
-  repos/user/repo/commits - C
    -  users/user/%committer%
    -  users//user/%author%


# commit_comments
- repos/user/repo/comments - CC
    - users/user/%user%


# PR
- repos/user/repo/pulls - P
    - repos/user/repo/commit/base
        -  users/user/%committer%
        -  users//user/%author%
    - repos/user/repo/commit/head 
        -  users/user/%committer%
        -  users//user/%author%
    - users/user/%user% -> quien hizo la pr
    - users/user/%head.user% -> dueño del commit repo de la pr
    - users/user/%base.user% -> dueño del commit hacia donde va la pr.
    - users/user/%head.repo.owner% -> dueño del repo head
    - users/user/%base.repo.owner% -> dueño del commit base 
    - repos/user/repo/pulls/%number%/commits - PC [min 1, max 3]
        - users/user/%author%
        - users/user/%committer%


# PR comments
- repos/user/repo/pulls/comments - PCM
    - users/user/%user% -> quien hizo el comentario


# issue
- repos/user/repo/issues - I
    - users/user/%user%
    - users/user/%asssignee%
    - repos/user/repo/issues/number/events - IE
        - users/user/%actor%


# issue comments
- repos/user/repo/issues/comments - IC
    - users/user/%user%


# labels
- repos/user/repo/labels - L


# milestones
- repos/user/repo/milestones - M