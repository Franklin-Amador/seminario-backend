-- CreateTable
CREATE TABLE "mdl_user" (
    "id" SERIAL NOT NULL,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "firstname" TEXT NOT NULL,
    "lastname" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "auth" TEXT NOT NULL DEFAULT 'manual',
    "confirmed" BOOLEAN NOT NULL DEFAULT false,
    "lang" TEXT NOT NULL DEFAULT 'es',
    "timezone" TEXT NOT NULL DEFAULT '99',
    "firstaccess" TIMESTAMP(3),
    "lastaccess" TIMESTAMP(3),
    "lastlogin" TIMESTAMP(3),
    "currentlogin" TIMESTAMP(3),
    "deleted" BOOLEAN NOT NULL DEFAULT false,
    "suspended" BOOLEAN NOT NULL DEFAULT false,
    "mnethostid" INTEGER NOT NULL DEFAULT 1,
    "institution" TEXT,
    "department" TEXT,
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_user_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_course" (
    "id" SERIAL NOT NULL,
    "category" INTEGER NOT NULL,
    "sortorder" INTEGER NOT NULL,
    "fullname" TEXT NOT NULL,
    "shortname" TEXT NOT NULL,
    "idnumber" TEXT,
    "summary" TEXT,
    "format" TEXT NOT NULL DEFAULT 'topics',
    "showgrades" BOOLEAN NOT NULL DEFAULT true,
    "newsitems" INTEGER NOT NULL DEFAULT 5,
    "startdate" TIMESTAMP(3) NOT NULL,
    "enddate" TIMESTAMP(3),
    "visible" BOOLEAN NOT NULL DEFAULT true,
    "groupmode" INTEGER NOT NULL DEFAULT 0,
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_course_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_course_categories" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "idnumber" TEXT,
    "description" TEXT,
    "parent" INTEGER NOT NULL DEFAULT 0,
    "sortorder" INTEGER NOT NULL,
    "coursecount" INTEGER NOT NULL DEFAULT 0,
    "visible" BOOLEAN NOT NULL DEFAULT true,
    "visibleold" BOOLEAN NOT NULL DEFAULT true,
    "timemodified" TIMESTAMP(3) NOT NULL,
    "depth" INTEGER NOT NULL,
    "path" TEXT NOT NULL,
    "theme" TEXT,

    CONSTRAINT "mdl_course_categories_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_course_category_map" (
    "category" INTEGER NOT NULL,
    "course" INTEGER NOT NULL,

    CONSTRAINT "mdl_course_category_map_pkey" PRIMARY KEY ("category","course")
);

-- CreateTable
CREATE TABLE "mdl_course_sections" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "section" INTEGER NOT NULL,
    "name" TEXT,
    "summary" TEXT,
    "sequence" TEXT,
    "visible" BOOLEAN NOT NULL DEFAULT true,
    "availability" TEXT,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_course_sections_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_modules" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "cron" INTEGER NOT NULL DEFAULT 0,
    "lastcron" TIMESTAMP(3),
    "search" TEXT,
    "visible" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "mdl_modules_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_course_modules" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "module" INTEGER NOT NULL,
    "instance" INTEGER NOT NULL,
    "section" INTEGER NOT NULL,
    "idnumber" TEXT,
    "added" TIMESTAMP(3) NOT NULL,
    "score" INTEGER NOT NULL DEFAULT 0,
    "indent" INTEGER NOT NULL DEFAULT 0,
    "visible" BOOLEAN NOT NULL DEFAULT true,
    "visibleoncoursepage" BOOLEAN NOT NULL DEFAULT true,
    "visibleold" BOOLEAN NOT NULL DEFAULT true,
    "groupmode" INTEGER NOT NULL DEFAULT 0,
    "groupingid" INTEGER NOT NULL DEFAULT 0,
    "completion" INTEGER NOT NULL DEFAULT 0,
    "completiongradeitemnumber" INTEGER,
    "completionview" BOOLEAN NOT NULL DEFAULT false,
    "completionexpected" TIMESTAMP(3),
    "availability" TEXT,
    "showdescription" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "mdl_course_modules_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_role" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "shortname" TEXT NOT NULL,
    "description" TEXT,
    "sortorder" INTEGER NOT NULL,
    "archetype" TEXT,

    CONSTRAINT "mdl_role_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_role_assignments" (
     "id" SERIAL NOT NULL,
        "roleid" INTEGER NOT NULL,
        "contextid" INTEGER NOT NULL,
        "userid" INTEGER NOT NULL,
        "timemodified" TIMESTAMP(3) NOT NULL,
        "modifierid" INTEGER NOT NULL,
        "component" TEXT,
        "itemid" INTEGER NOT NULL DEFAULT 0,
        "sortorder" INTEGER NOT NULL DEFAULT 0,

        CONSTRAINT "mdl_role_assignments_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_user_enrolments" (
    "id" SERIAL NOT NULL,
    "enrolid" INTEGER NOT NULL,
    "userid" INTEGER NOT NULL,
    "courseid" INTEGER NOT NULL,
    "status" INTEGER NOT NULL DEFAULT 0,
    "timestart" TIMESTAMP(3),
    "timeend" TIMESTAMP(3),
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_user_enrolments_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_assign" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "intro" TEXT NOT NULL,
    "introformat" INTEGER NOT NULL DEFAULT 0,
    "section" INTEGER NOT NULL,
    "alwaysshowdescription" BOOLEAN NOT NULL DEFAULT true,
    "nosubmissions" BOOLEAN NOT NULL DEFAULT false,
    "submissiondrafts" BOOLEAN NOT NULL DEFAULT false,
    "sendnotifications" BOOLEAN NOT NULL DEFAULT false,
    "sendlatenotifications" BOOLEAN NOT NULL DEFAULT false,
    "duedate" TIMESTAMP(3),
    "allowsubmissionsfromdate" TIMESTAMP(3),
    "grade" INTEGER,
    "timemodified" TIMESTAMP(3) NOT NULL,
    "requiresubmissionstatement" BOOLEAN NOT NULL DEFAULT false,
    "completionsubmit" BOOLEAN NOT NULL DEFAULT false,
    "cutoffdate" TIMESTAMP(3),
    "gradingduedate" TIMESTAMP(3),
    "teamsubmission" BOOLEAN NOT NULL DEFAULT false,
    "requireallteammemberssubmit" BOOLEAN NOT NULL DEFAULT false,
    "teamsubmissiongroupingid" INTEGER NOT NULL DEFAULT 0,
    "blindmarking" BOOLEAN NOT NULL DEFAULT false,
    "revealidentities" BOOLEAN NOT NULL DEFAULT false,
    "attemptreopenmethod" TEXT NOT NULL DEFAULT 'none',
    "maxattempts" INTEGER NOT NULL DEFAULT -1,
    "markingworkflow" BOOLEAN NOT NULL DEFAULT false,
    "markingallocation" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "mdl_assign_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_assign_submission" (
    "id" SERIAL NOT NULL,
    "assignment" INTEGER NOT NULL,
    "userid" INTEGER NOT NULL,
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,
    "status" TEXT NOT NULL,
    "groupid" INTEGER NOT NULL DEFAULT 0,
    "attemptnumber" INTEGER NOT NULL DEFAULT 0,
    "latest" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "mdl_assign_submission_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_quiz" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "intro" TEXT NOT NULL,
    "introformat" INTEGER NOT NULL DEFAULT 0,
    "timeopen" TIMESTAMP(3),
    "timeclose" TIMESTAMP(3),
    "timelimit" INTEGER,
    "preferredbehaviour" TEXT NOT NULL,
    "attempts" INTEGER NOT NULL DEFAULT 0,
    "grademethod" INTEGER NOT NULL DEFAULT 1,
    "decimalpoints" INTEGER NOT NULL DEFAULT 2,
    "questiondecimalpoints" INTEGER NOT NULL DEFAULT -1,
    "sumgrades" INTEGER NOT NULL DEFAULT 0,
    "grade" INTEGER NOT NULL DEFAULT 0,
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,
    "password" TEXT,
    "subnet" TEXT,
    "browsersecurity" TEXT,
    "delay1" INTEGER NOT NULL DEFAULT 0,
    "delay2" INTEGER NOT NULL DEFAULT 0,
    "showuserpicture" INTEGER NOT NULL DEFAULT 0,
    "showblocks" INTEGER NOT NULL DEFAULT 0,
    "navmethod" TEXT NOT NULL DEFAULT 'free',
    "shuffleanswers" INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT "mdl_quiz_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_course_completions" (
    "id" SERIAL NOT NULL,
    "userid" INTEGER NOT NULL,
    "course" INTEGER NOT NULL,
    "timeenrolled" TIMESTAMP(3) NOT NULL,
    "timestarted" TIMESTAMP(3) NOT NULL,
    "timecompleted" TIMESTAMP(3),
    "reaggregate" TIMESTAMP(3),

    CONSTRAINT "mdl_course_completions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_forum" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "type" TEXT NOT NULL DEFAULT 'general',
    "name" TEXT NOT NULL,
    "intro" TEXT NOT NULL,
    "introformat" INTEGER NOT NULL DEFAULT 0,
    "assessed" INTEGER NOT NULL DEFAULT 0,
    "assesstimestart" TIMESTAMP(3),
    "assesstimefinish" TIMESTAMP(3),
    "scale" INTEGER NOT NULL DEFAULT 0,
    "maxbytes" INTEGER NOT NULL DEFAULT 0,
    "maxattachments" INTEGER NOT NULL DEFAULT 1,
    "forcesubscribe" INTEGER NOT NULL DEFAULT 0,
    "trackingtype" INTEGER NOT NULL DEFAULT 1,
    "rsstype" INTEGER NOT NULL DEFAULT 0,
    "rssarticles" INTEGER NOT NULL DEFAULT 0,
    "timemodified" TIMESTAMP(3) NOT NULL,
    "warnafter" INTEGER NOT NULL DEFAULT 0,
    "blockafter" INTEGER NOT NULL DEFAULT 0,
    "blockperiod" INTEGER NOT NULL DEFAULT 0,
    "completiondiscussions" INTEGER NOT NULL DEFAULT 0,
    "completionreplies" INTEGER NOT NULL DEFAULT 0,
    "completionposts" INTEGER NOT NULL DEFAULT 0,
    "displaywordcount" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "mdl_forum_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_forum_discussions" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "forum" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "firstpost" INTEGER NOT NULL,
    "userid" INTEGER NOT NULL,
    "groupid" INTEGER NOT NULL DEFAULT -1,
    "assessed" BOOLEAN NOT NULL DEFAULT true,
    "timemodified" TIMESTAMP(3) NOT NULL,
    "usermodified" INTEGER NOT NULL DEFAULT 0,
    "timestart" TIMESTAMP(3),
    "timeend" TIMESTAMP(3),
    "pinned" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "mdl_forum_discussions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_forum_posts" (
    "id" SERIAL NOT NULL,
    "discussion" INTEGER NOT NULL,
    "parent" INTEGER NOT NULL DEFAULT 0,
    "userid" INTEGER NOT NULL,
    "created" TIMESTAMP(3) NOT NULL,
    "modified" TIMESTAMP(3) NOT NULL,
    "mailed" INTEGER NOT NULL DEFAULT 0,
    "subject" TEXT NOT NULL,
    "message" TEXT NOT NULL,
    "messageformat" INTEGER NOT NULL DEFAULT 0,
    "messagetrust" INTEGER NOT NULL DEFAULT 0,
    "attachment" TEXT,
    "totalscore" INTEGER NOT NULL DEFAULT 0,
    "mailnow" INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT "mdl_forum_posts_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_grade_items" (
    "id" SERIAL NOT NULL,
    "courseid" INTEGER NOT NULL,
    "categoryid" INTEGER,
    "itemname" TEXT,
    "itemtype" TEXT NOT NULL,
    "itemmodule" TEXT,
    "iteminstance" INTEGER,
    "itemnumber" INTEGER,
    "iteminfo" TEXT,
    "idnumber" TEXT,
    "calculation" TEXT,
    "gradetype" INTEGER NOT NULL DEFAULT 1,
    "grademax" DECIMAL(10,5) NOT NULL DEFAULT 100,
    "grademin" DECIMAL(10,5) NOT NULL DEFAULT 0,
    "scaleid" INTEGER,
    "outcomeid" INTEGER,
    "gradepass" DECIMAL(10,5) NOT NULL DEFAULT 0,
    "multfactor" DECIMAL(10,5) NOT NULL DEFAULT 1,
    "plusfactor" DECIMAL(10,5) NOT NULL DEFAULT 0,
    "aggregationcoef" DECIMAL(10,5) NOT NULL DEFAULT 0,
    "aggregationcoef2" DECIMAL(10,5) NOT NULL DEFAULT 0,
    "sortorder" INTEGER NOT NULL DEFAULT 0,
    "display" INTEGER NOT NULL DEFAULT 0,
    "decimals" INTEGER,
    "hidden" INTEGER NOT NULL DEFAULT 0,
    "locked" INTEGER NOT NULL DEFAULT 0,
    "locktime" TIMESTAMP(3),
    "needsupdate" INTEGER NOT NULL DEFAULT 0,
    "weightoverride" INTEGER NOT NULL DEFAULT 0,
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_grade_items_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_grade_grades" (
    "id" SERIAL NOT NULL,
    "itemid" INTEGER NOT NULL,
    "userid" INTEGER NOT NULL,
    "rawgrade" INTEGER,
    "rawgrademax" INTEGER NOT NULL DEFAULT 100,
    "rawgrademin" INTEGER NOT NULL DEFAULT 0,
    "finalgrade" INTEGER,
    "hidden" INTEGER NOT NULL DEFAULT 0,
    "locked" INTEGER NOT NULL DEFAULT 0,
    "locktime" TIMESTAMP(3),
    "exported" INTEGER NOT NULL DEFAULT 0,
    "overridden" INTEGER NOT NULL DEFAULT 0,
    "excluded" INTEGER NOT NULL DEFAULT 0,
    "feedback" TEXT,
    "feedbackformat" INTEGER NOT NULL DEFAULT 0,
    "information" TEXT,
    "informationformat" INTEGER NOT NULL DEFAULT 0,
    "timecreated" TIMESTAMP(3) NOT NULL,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_grade_grades_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_resource" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "intro" TEXT,
    "introformat" INTEGER NOT NULL DEFAULT 0,
    "tobemigrated" INTEGER NOT NULL DEFAULT 0,
    "legacyfiles" INTEGER NOT NULL DEFAULT 0,
    "legacyfileslast" INTEGER,
    "display" INTEGER NOT NULL DEFAULT 0,
    "displayoptions" TEXT,
    "filterfiles" INTEGER NOT NULL DEFAULT 0,
    "revision" INTEGER NOT NULL DEFAULT 0,
    "timemodified" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "mdl_resource_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "mdl_scorm" (
    "id" SERIAL NOT NULL,
    "course" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "scormtype" TEXT NOT NULL DEFAULT 'local',
    "reference" TEXT NOT NULL,
    "intro" TEXT NOT NULL,
    "introformat" INTEGER NOT NULL DEFAULT 0,
    "version" TEXT NOT NULL,
    "maxgrade" INTEGER NOT NULL DEFAULT 0,
    "grademethod" INTEGER NOT NULL DEFAULT 0,
    "whatgrade" INTEGER NOT NULL DEFAULT 0,
    "maxattempt" INTEGER NOT NULL DEFAULT 1,
    "forcecompleted" BOOLEAN NOT NULL DEFAULT false,
    "forcenewattempt" INTEGER NOT NULL DEFAULT 0,
    "lastattemptlock" BOOLEAN NOT NULL DEFAULT false,
    "masteryoverride" BOOLEAN NOT NULL DEFAULT true,
    "displayattemptstatus" INTEGER NOT NULL DEFAULT 1,
    "displaycoursestructure" BOOLEAN NOT NULL DEFAULT false,
    "updatefreq" INTEGER NOT NULL DEFAULT 0,
    "sha1hash" TEXT,
    "md5hash" TEXT,
    "revision" INTEGER NOT NULL DEFAULT 0,
    "launch" INTEGER NOT NULL DEFAULT 0,
    "skipview" INTEGER NOT NULL DEFAULT 1,
    "hidebrowse" BOOLEAN NOT NULL DEFAULT false,
    "hidetoc" INTEGER NOT NULL DEFAULT 0,
    "nav" INTEGER NOT NULL DEFAULT 1,
    "navpositionleft" INTEGER,
    "navpositiontop" INTEGER,
    "auto" BOOLEAN NOT NULL DEFAULT false,
    "popup" BOOLEAN NOT NULL DEFAULT false,
    "width" INTEGER NOT NULL DEFAULT 100,
    "height" INTEGER NOT NULL DEFAULT 600,
    "timeopen" TIMESTAMP(3),
    "timeclose" TIMESTAMP(3),
    "timemodified" TIMESTAMP(3) NOT NULL,
    "completionstatusrequired" INTEGER,
    "completionscorerequired" INTEGER,
    "completionstatusallscos" INTEGER,
    "autocommit" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "mdl_scorm_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "mdl_user_username_key" ON "mdl_user"("username");

-- CreateIndex
CREATE UNIQUE INDEX "mdl_user_email_key" ON "mdl_user"("email");

-- CreateIndex
CREATE UNIQUE INDEX "mdl_modules_name_key" ON "mdl_modules"("name");

-- CreateIndex
CREATE UNIQUE INDEX "mdl_role_shortname_key" ON "mdl_role"("shortname");

-- AddForeignKey
ALTER TABLE "mdl_course_category_map" ADD CONSTRAINT "mdl_course_category_map_category_fkey" FOREIGN KEY ("category") REFERENCES "mdl_course_categories"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_course_category_map" ADD CONSTRAINT "mdl_course_category_map_course_fkey" FOREIGN KEY ("course") REFERENCES "mdl_course"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_course_sections" ADD CONSTRAINT "mdl_course_sections_course_fkey" FOREIGN KEY ("course") REFERENCES "mdl_course"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_course_modules" ADD CONSTRAINT "mdl_course_modules_course_fkey" FOREIGN KEY ("course") REFERENCES "mdl_course"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_course_modules" ADD CONSTRAINT "mdl_course_modules_module_fkey" FOREIGN KEY ("module") REFERENCES "mdl_modules"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_role_assignments" ADD CONSTRAINT "mdl_role_assignments_roleid_fkey" FOREIGN KEY ("roleid") REFERENCES "mdl_role"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_role_assignments" ADD CONSTRAINT "mdl_role_assignments_userid_fkey" FOREIGN KEY ("userid") REFERENCES "mdl_user"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_user_enrolments" ADD CONSTRAINT "mdl_user_enrolments_userid_fkey" FOREIGN KEY ("userid") REFERENCES "mdl_user"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_user_enrolments" ADD CONSTRAINT "mdl_user_enrolments_courseid_fkey" FOREIGN KEY ("courseid") REFERENCES "mdl_course"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_assign_submission" ADD CONSTRAINT "mdl_assign_submission_assignment_fkey" FOREIGN KEY ("assignment") REFERENCES "mdl_assign"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_assign_submission" ADD CONSTRAINT "mdl_assign_submission_userid_fkey" FOREIGN KEY ("userid") REFERENCES "mdl_user"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_course_completions" ADD CONSTRAINT "mdl_course_completions_userid_fkey" FOREIGN KEY ("userid") REFERENCES "mdl_user"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_course_completions" ADD CONSTRAINT "mdl_course_completions_course_fkey" FOREIGN KEY ("course") REFERENCES "mdl_course"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_forum_discussions" ADD CONSTRAINT "mdl_forum_discussions_forum_fkey" FOREIGN KEY ("forum") REFERENCES "mdl_forum"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_forum_posts" ADD CONSTRAINT "mdl_forum_posts_discussion_fkey" FOREIGN KEY ("discussion") REFERENCES "mdl_forum_discussions"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "mdl_grade_grades" ADD CONSTRAINT "mdl_grade_grades_itemid_fkey" FOREIGN KEY ("itemid") REFERENCES "mdl_grade_items"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE "mdl_assign" ADD CONSTRAINT "mdl_assign_section_fkey" FOREIGN KEY ("section") REFERENCES "mdl_course_sections"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
