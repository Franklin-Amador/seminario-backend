-- CreateTable
CREATE TABLE `mdl_user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `firstname` VARCHAR(255) NOT NULL,
    `lastname` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `auth` VARCHAR(255) NOT NULL DEFAULT 'manual',
    `confirmed` TINYINT(1) NOT NULL DEFAULT 0,
    `lang` VARCHAR(255) NOT NULL DEFAULT 'es',
    `timezone` VARCHAR(255) NOT NULL DEFAULT '99',
    `firstaccess` DATETIME NULL,
    `lastaccess` DATETIME NULL,
    `lastlogin` DATETIME NULL,
    `currentlogin` DATETIME NULL,
    `deleted` TINYINT(1) NOT NULL DEFAULT 0,
    `suspended` TINYINT(1) NOT NULL DEFAULT 0,
    `mnethostid` INT NOT NULL DEFAULT 1,
    `institution` VARCHAR(255) NULL,
    `department` VARCHAR(255) NULL,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,

    UNIQUE INDEX `mdl_user_username_key` (`username`),
    UNIQUE INDEX `mdl_user_email_key` (`email`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_course` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `category` INT NOT NULL,
    `sortorder` INT NOT NULL,
    `fullname` VARCHAR(255) NOT NULL,
    `shortname` VARCHAR(255) NOT NULL,
    `idnumber` VARCHAR(255) NULL,
    `summary` TEXT NULL,
    `format` VARCHAR(255) NOT NULL DEFAULT 'topics',
    `showgrades` TINYINT(1) NOT NULL DEFAULT 1,
    `newsitems` INT NOT NULL DEFAULT 5,
    `startdate` DATETIME NOT NULL,
    `enddate` DATETIME NULL,
    `visible` TINYINT(1) NOT NULL DEFAULT 1,
    `groupmode` INT NOT NULL DEFAULT 0,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_course_categories` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `idnumber` VARCHAR(255) NULL,
    `description` TEXT NULL,
    `parent` INT NOT NULL DEFAULT 0,
    `sortorder` INT NOT NULL,
    `coursecount` INT NOT NULL DEFAULT 0,
    `visible` TINYINT(1) NOT NULL DEFAULT 1,
    `visibleold` TINYINT(1) NOT NULL DEFAULT 1,
    `timemodified` DATETIME NOT NULL,
    `depth` INT NOT NULL,
    `path` VARCHAR(255) NOT NULL,
    `theme` VARCHAR(255) NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_course_category_map` (
    `category` INT NOT NULL,
    `course` INT NOT NULL,

    PRIMARY KEY (`category`, `course`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_course_sections` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `section` INT NOT NULL,
    `name` VARCHAR(255) NULL,
    `summary` TEXT NULL,
    `sequence` TEXT NULL,
    `visible` TINYINT(1) NOT NULL DEFAULT 1,
    `availability` TEXT NULL,
    `timemodified` DATETIME NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_modules` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `cron` INT NOT NULL DEFAULT 0,
    `lastcron` DATETIME NULL,
    `search` TEXT NULL,
    `visible` TINYINT(1) NOT NULL DEFAULT 1,

    UNIQUE INDEX `mdl_modules_name_key` (`name`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_course_modules` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `module` INT NOT NULL,
    `instance` INT NOT NULL,
    `section` INT NOT NULL,
    `idnumber` VARCHAR(255) NULL,
    `added` DATETIME NOT NULL,
    `score` INT NOT NULL DEFAULT 0,
    `indent` INT NOT NULL DEFAULT 0,
    `visible` TINYINT(1) NOT NULL DEFAULT 1,
    `visibleoncoursepage` TINYINT(1) NOT NULL DEFAULT 1,
    `visibleold` TINYINT(1) NOT NULL DEFAULT 1,
    `groupmode` INT NOT NULL DEFAULT 0,
    `groupingid` INT NOT NULL DEFAULT 0,
    `completion` INT NOT NULL DEFAULT 0,
    `completiongradeitemnumber` INT NULL,
    `completionview` TINYINT(1) NOT NULL DEFAULT 0,
    `completionexpected` DATETIME NULL,
    `availability` TEXT NULL,
    `showdescription` TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_role` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `shortname` VARCHAR(255) NOT NULL,
    `description` TEXT NULL,
    `sortorder` INT NOT NULL,
    `archetype` VARCHAR(255) NULL,

    UNIQUE INDEX `mdl_role_shortname_key` (`shortname`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_role_assignments` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `roleid` INT NOT NULL,
    `contextid` INT NOT NULL,
    `userid` INT NOT NULL,
    `timemodified` DATETIME NOT NULL,
    `modifierid` INT NOT NULL,
    `component` VARCHAR(255) NULL,
    `itemid` INT NOT NULL DEFAULT 0,
    `sortorder` INT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_user_enrolments` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `enrolid` INT NOT NULL,
    `userid` INT NOT NULL,
    `courseid` INT NOT NULL,
    `status` INT NOT NULL DEFAULT 0,
    `timestart` DATETIME NULL,
    `timeend` DATETIME NULL,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_assign` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `intro` TEXT NOT NULL,
    `introformat` INT NOT NULL DEFAULT 0,
    `alwaysshowdescription` TINYINT(1) NOT NULL DEFAULT 1,
    `nosubmissions` TINYINT(1) NOT NULL DEFAULT 0,
    `submissiondrafts` TINYINT(1) NOT NULL DEFAULT 0,
    `sendnotifications` TINYINT(1) NOT NULL DEFAULT 0,
    `sendlatenotifications` TINYINT(1) NOT NULL DEFAULT 0,
    `duedate` DATETIME NULL,
    `allowsubmissionsfromdate` DATETIME NULL,
    `grade` INT NULL,
    `timemodified` DATETIME NOT NULL,
    `requiresubmissionstatement` TINYINT(1) NOT NULL DEFAULT 0,
    `completionsubmit` TINYINT(1) NOT NULL DEFAULT 0,
    `cutoffdate` DATETIME NULL,
    `gradingduedate` DATETIME NULL,
    `teamsubmission` TINYINT(1) NOT NULL DEFAULT 0,
    `requireallteammemberssubmit` TINYINT(1) NOT NULL DEFAULT 0,
    `teamsubmissiongroupingid` INT NOT NULL DEFAULT 0,
    `blindmarking` TINYINT(1) NOT NULL DEFAULT 0,
    `revealidentities` TINYINT(1) NOT NULL DEFAULT 0,
    `attemptreopenmethod` VARCHAR(255) NOT NULL DEFAULT 'none',
    `maxattempts` INT NOT NULL DEFAULT -1,
    `markingworkflow` TINYINT(1) NOT NULL DEFAULT 0,
    `markingallocation` TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_assign_submission` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `assignment` INT NOT NULL,
    `userid` INT NOT NULL,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,
    `status` VARCHAR(255) NOT NULL,
    `groupid` INT NOT NULL DEFAULT 0,
    `attemptnumber` INT NOT NULL DEFAULT 0,
    `latest` TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_quiz` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `intro` TEXT NOT NULL,
    `introformat` INT NOT NULL DEFAULT 0,
    `timeopen` DATETIME NULL,
    `timeclose` DATETIME NULL,
    `timelimit` INT NULL,
    `preferredbehaviour` VARCHAR(255) NOT NULL,
    `attempts` INT NOT NULL DEFAULT 0,
    `grademethod` INT NOT NULL DEFAULT 1,
    `decimalpoints` INT NOT NULL DEFAULT 2,
    `questiondecimalpoints` INT NOT NULL DEFAULT -1,
    `sumgrades` INT NOT NULL DEFAULT 0,
    `grade` INT NOT NULL DEFAULT 0,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,
    `password` VARCHAR(255) NULL,
    `subnet` VARCHAR(255) NULL,
    `browsersecurity` VARCHAR(255) NULL,
    `delay1` INT NOT NULL DEFAULT 0,
    `delay2` INT NOT NULL DEFAULT 0,
    `showuserpicture` INT NOT NULL DEFAULT 0,
    `showblocks` INT NOT NULL DEFAULT 0,
    `navmethod` VARCHAR(255) NOT NULL DEFAULT 'free',
    `shuffleanswers` INT NOT NULL DEFAULT 1,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_course_completions` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `userid` INT NOT NULL,
    `course` INT NOT NULL,
    `timeenrolled` DATETIME NOT NULL,
    `timestarted` DATETIME NOT NULL,
    `timecompleted` DATETIME NULL,
    `reaggregate` DATETIME NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_forum` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `type` VARCHAR(255) NOT NULL DEFAULT 'general',
    `name` VARCHAR(255) NOT NULL,
    `intro` TEXT NOT NULL,
    `introformat` INT NOT NULL DEFAULT 0,
    `assessed` INT NOT NULL DEFAULT 0,
    `assesstimestart` DATETIME NULL,
    `assesstimefinish` DATETIME NULL,
    `scale` INT NOT NULL DEFAULT 0,
    `maxbytes` INT NOT NULL DEFAULT 0,
    `maxattachments` INT NOT NULL DEFAULT 1,
    `forcesubscribe` INT NOT NULL DEFAULT 0,
    `trackingtype` INT NOT NULL DEFAULT 1,
    `rsstype` INT NOT NULL DEFAULT 0,
    `rssarticles` INT NOT NULL DEFAULT 0,
    `timemodified` DATETIME NOT NULL,
    `warnafter` INT NOT NULL DEFAULT 0,
    `blockafter` INT NOT NULL DEFAULT 0,
    `blockperiod` INT NOT NULL DEFAULT 0,
    `completiondiscussions` INT NOT NULL DEFAULT 0,
    `completionreplies` INT NOT NULL DEFAULT 0,
    `completionposts` INT NOT NULL DEFAULT 0,
    `displaywordcount` TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_forum_discussions` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `forum` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `firstpost` INT NOT NULL,
    `userid` INT NOT NULL,
    `groupid` INT NOT NULL DEFAULT -1,
    `assessed` TINYINT(1) NOT NULL DEFAULT 1,
    `timemodified` DATETIME NOT NULL,
    `usermodified` INT NOT NULL DEFAULT 0,
    `timestart` DATETIME NULL,
    `timeend` DATETIME NULL,
    `pinned` TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_forum_posts` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `discussion` INT NOT NULL,
    `parent` INT NOT NULL DEFAULT 0,
    `userid` INT NOT NULL,
    `created` DATETIME NOT NULL,
    `modified` DATETIME NOT NULL,
    `mailed` INT NOT NULL DEFAULT 0,
    `subject` VARCHAR(255) NOT NULL,
    `message` TEXT NOT NULL,
    `messageformat` INT NOT NULL DEFAULT 0,
    `messagetrust` INT NOT NULL DEFAULT 0,
    `attachment` VARCHAR(255) NULL,
    `totalscore` INT NOT NULL DEFAULT 0,
    `mailnow` INT NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_grade_items` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `courseid` INT NOT NULL,
    `categoryid` INT NULL,
    `itemname` VARCHAR(255) NULL,
    `itemtype` VARCHAR(255) NOT NULL,
    `itemmodule` VARCHAR(255) NULL,
    `iteminstance` INT NULL,
    `itemnumber` INT NULL,
    `iteminfo` TEXT NULL,
    `idnumber` VARCHAR(255) NULL,
    `calculation` TEXT NULL,
    `gradetype` INT NOT NULL DEFAULT 1,
    `grademax` DECIMAL(10,5) NOT NULL DEFAULT 100.00000,
    `grademin` DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    `scaleid` INT NULL,
    `outcomeid` INT NULL,
    `gradepass` DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    `multfactor` DECIMAL(10,5) NOT NULL DEFAULT 1.00000,
    `plusfactor` DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    `aggregationcoef` DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    `aggregationcoef2` DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    `sortorder` INT NOT NULL DEFAULT 0,
    `display` INT NOT NULL DEFAULT 0,
    `decimals` INT NULL,
    `hidden` INT NOT NULL DEFAULT 0,
    `locked` INT NOT NULL DEFAULT 0,
    `locktime` DATETIME NULL,
    `needsupdate` INT NOT NULL DEFAULT 0,
    `weightoverride` INT NOT NULL DEFAULT 0,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_grade_grades` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `itemid` INT NOT NULL,
    `userid` INT NOT NULL,
    `rawgrade` INT NULL,
    `rawgrademax` INT NOT NULL DEFAULT 100,
    `rawgrademin` INT NOT NULL DEFAULT 0,
    `finalgrade` INT NULL,
    `hidden` INT NOT NULL DEFAULT 0,
    `locked` INT NOT NULL DEFAULT 0,
    `locktime` DATETIME NULL,
    `exported` INT NOT NULL DEFAULT 0,
    `overridden` INT NOT NULL DEFAULT 0,
    `excluded` INT NOT NULL DEFAULT 0,
    `feedback` TEXT NULL,
    `feedbackformat` INT NOT NULL DEFAULT 0,
    `information` TEXT NULL,
    `informationformat` INT NOT NULL DEFAULT 0,
    `timecreated` DATETIME NOT NULL,
    `timemodified` DATETIME NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_resource` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `intro` TEXT NULL,
    `introformat` INT NOT NULL DEFAULT 0,
    `tobemigrated` INT NOT NULL DEFAULT 0,
    `legacyfiles` INT NOT NULL DEFAULT 0,
    `legacyfileslast` INT NULL,
    `display` INT NOT NULL DEFAULT 0,
    `displayoptions` TEXT NULL,
    `filterfiles` INT NOT NULL DEFAULT 0,
    `revision` INT NOT NULL DEFAULT 0,
    `timemodified` DATETIME NOT NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `mdl_scorm` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `course` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `scormtype` VARCHAR(255) NOT NULL DEFAULT 'local',
    `reference` VARCHAR(255) NOT NULL,
    `intro` TEXT NOT NULL,
    `introformat` INT NOT NULL DEFAULT 0,
    `version` VARCHAR(255) NOT NULL,
    `maxgrade` INT NOT NULL DEFAULT 0,
    `grademethod` INT NOT NULL DEFAULT 0,
    `whatgrade` INT NOT NULL DEFAULT 0,
    `maxattempt` INT NOT NULL DEFAULT 1,
    `forcecompleted` TINYINT(1) NOT NULL DEFAULT 0,
    `forcenewattempt` INT NOT NULL DEFAULT 0,
    `lastattemptlock` TINYINT(1) NOT NULL DEFAULT 0,
    `masteryoverride` TINYINT(1) NOT NULL DEFAULT 1,
    `displayattemptstatus` INT NOT NULL DEFAULT 1,
    `displaycoursestructure` TINYINT(1) NOT NULL DEFAULT 0,
    `updatefreq` INT NOT NULL DEFAULT 0,
    `sha1hash` VARCHAR(255) NULL,
    `md5hash` VARCHAR(255) NULL,
    `revision` INT NOT NULL DEFAULT 0,
    `launch` INT NOT NULL DEFAULT 0,
    `skipview` INT NOT NULL DEFAULT 1,
    `hidebrowse` TINYINT(1) NOT NULL DEFAULT 0,
    `hidetoc` INT NOT NULL DEFAULT 0,
    `nav` INT NOT NULL DEFAULT 1,
    `navpositionleft` INT NULL,
    `navpositiontop` INT NULL,
    `auto` TINYINT(1) NOT NULL DEFAULT 0,
    `popup` TINYINT(1) NOT NULL DEFAULT 0,
    `width` INT NOT NULL DEFAULT 100,
    `height` INT NOT NULL DEFAULT 600,
    `timeopen` DATETIME NULL,
    `timeclose` DATETIME NULL,
    `timemodified` DATETIME NOT NULL,
    `completionstatusrequired` INT NULL,
    `completionscorerequired` INT NULL,
    `completionstatusallscos` INT NULL,
    `autocommit` TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `mdl_course_category_map` ADD CONSTRAINT `mdl_course_category_map_category_fkey` FOREIGN KEY (`category`) REFERENCES `mdl_course_categories`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_course_category_map` ADD CONSTRAINT `mdl_course_category_map_course_fkey` FOREIGN KEY (`course`) REFERENCES `mdl_course`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_course_sections` ADD CONSTRAINT `mdl_course_sections_course_fkey` FOREIGN KEY (`course`) REFERENCES `mdl_course`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_course_modules` ADD CONSTRAINT `mdl_course_modules_course_fkey` FOREIGN KEY (`course`) REFERENCES `mdl_course`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_course_modules` ADD CONSTRAINT `mdl_course_modules_module_fkey` FOREIGN KEY (`module`) REFERENCES `mdl_modules`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_role_assignments` ADD CONSTRAINT `mdl_role_assignments_roleid_fkey` FOREIGN KEY (`roleid`) REFERENCES `mdl_role`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_role_assignments` ADD CONSTRAINT `mdl_role_assignments_userid_fkey` FOREIGN KEY (`userid`) REFERENCES `mdl_user`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_user_enrolments` ADD CONSTRAINT `mdl_user_enrolments_userid_fkey` FOREIGN KEY (`userid`) REFERENCES `mdl_user`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_user_enrolments` ADD CONSTRAINT `mdl_user_enrolments_courseid_fkey` FOREIGN KEY (`courseid`) REFERENCES `mdl_course`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_assign_submission` ADD CONSTRAINT `mdl_assign_submission_assignment_fkey` FOREIGN KEY (`assignment`) REFERENCES `mdl_assign`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_assign_submission` ADD CONSTRAINT `mdl_assign_submission_userid_fkey` FOREIGN KEY (`userid`) REFERENCES `mdl_user`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_course_completions` ADD CONSTRAINT `mdl_course_completions_userid_fkey` FOREIGN KEY (`userid`) REFERENCES `mdl_user`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_course_completions` ADD CONSTRAINT `mdl_course_completions_course_fkey` FOREIGN KEY (`course`) REFERENCES `mdl_course`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_forum_discussions` ADD CONSTRAINT `mdl_forum_discussions_forum_fkey` FOREIGN KEY (`forum`) REFERENCES `mdl_forum`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_forum_posts` ADD CONSTRAINT `mdl_forum_posts_discussion_fkey` FOREIGN KEY (`discussion`) REFERENCES `mdl_forum_discussions`(`id`);

-- AddForeignKey
ALTER TABLE `mdl_grade_grades` ADD CONSTRAINT `mdl_grade_grades_itemid_fkey` FOREIGN KEY (`itemid`) REFERENCES `mdl_grade_items`(`id`);
