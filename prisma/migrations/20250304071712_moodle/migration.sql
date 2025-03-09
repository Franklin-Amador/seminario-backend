-- CreateTable
CREATE TABLE [mdl_user] (
    [id] INT NOT NULL IDENTITY(1,1),
    [username] NVARCHAR(255) NOT NULL,
    [password] NVARCHAR(255) NOT NULL,
    [firstname] NVARCHAR(255) NOT NULL,
    [lastname] NVARCHAR(255) NOT NULL,
    [email] NVARCHAR(255) NOT NULL,
    [auth] NVARCHAR(255) NOT NULL DEFAULT 'manual',
    [confirmed] BIT NOT NULL DEFAULT 0,
    [lang] NVARCHAR(255) NOT NULL DEFAULT 'es',
    [timezone] NVARCHAR(255) NOT NULL DEFAULT '99',
    [firstaccess] DATETIME2 NULL,
    [lastaccess] DATETIME2 NULL,
    [lastlogin] DATETIME2 NULL,
    [currentlogin] DATETIME2 NULL,
    [deleted] BIT NOT NULL DEFAULT 0,
    [suspended] BIT NOT NULL DEFAULT 0,
    [mnethostid] INT NOT NULL DEFAULT 1,
    [institution] NVARCHAR(255) NULL,
    [department] NVARCHAR(255) NULL,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_user] PRIMARY KEY ([id]),
    CONSTRAINT [UK_mdl_user_username] UNIQUE ([username]),
    CONSTRAINT [UK_mdl_user_email] UNIQUE ([email])
);

-- CreateTable
CREATE TABLE [mdl_course] (
    [id] INT NOT NULL IDENTITY(1,1),
    [category] INT NOT NULL,
    [sortorder] INT NOT NULL,
    [fullname] NVARCHAR(255) NOT NULL,
    [shortname] NVARCHAR(255) NOT NULL,
    [idnumber] NVARCHAR(255) NULL,
    [summary] NVARCHAR(MAX) NULL,
    [format] NVARCHAR(255) NOT NULL DEFAULT 'topics',
    [showgrades] BIT NOT NULL DEFAULT 1,
    [newsitems] INT NOT NULL DEFAULT 5,
    [startdate] DATETIME2 NOT NULL,
    [enddate] DATETIME2 NULL,
    [visible] BIT NOT NULL DEFAULT 1,
    [groupmode] INT NOT NULL DEFAULT 0,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_course] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_course_categories] (
    [id] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(255) NOT NULL,
    [idnumber] NVARCHAR(255) NULL,
    [description] NVARCHAR(MAX) NULL,
    [parent] INT NOT NULL DEFAULT 0,
    [sortorder] INT NOT NULL,
    [coursecount] INT NOT NULL DEFAULT 0,
    [visible] BIT NOT NULL DEFAULT 1,
    [visibleold] BIT NOT NULL DEFAULT 1,
    [timemodified] DATETIME2 NOT NULL,
    [depth] INT NOT NULL,
    [path] NVARCHAR(255) NOT NULL,
    [theme] NVARCHAR(255) NULL,
    CONSTRAINT [PK_mdl_course_categories] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_course_category_map] (
    [category] INT NOT NULL,
    [course] INT NOT NULL,
    CONSTRAINT [PK_mdl_course_category_map] PRIMARY KEY ([category], [course])
);

-- CreateTable
CREATE TABLE [mdl_course_sections] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [section] INT NOT NULL,
    [name] NVARCHAR(255) NULL,
    [summary] NVARCHAR(MAX) NULL,
    [sequence] NVARCHAR(MAX) NULL,
    [visible] BIT NOT NULL DEFAULT 1,
    [availability] NVARCHAR(MAX) NULL,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_course_sections] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_modules] (
    [id] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(255) NOT NULL,
    [cron] INT NOT NULL DEFAULT 0,
    [lastcron] DATETIME2 NULL,
    [search] NVARCHAR(MAX) NULL,
    [visible] BIT NOT NULL DEFAULT 1,
    CONSTRAINT [PK_mdl_modules] PRIMARY KEY ([id]),
    CONSTRAINT [UK_mdl_modules_name] UNIQUE ([name])
);

-- CreateTable
CREATE TABLE [mdl_course_modules] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [module] INT NOT NULL,
    [instance] INT NOT NULL,
    [section] INT NOT NULL,
    [idnumber] NVARCHAR(255) NULL,
    [added] DATETIME2 NOT NULL,
    [score] INT NOT NULL DEFAULT 0,
    [indent] INT NOT NULL DEFAULT 0,
    [visible] BIT NOT NULL DEFAULT 1,
    [visibleoncoursepage] BIT NOT NULL DEFAULT 1,
    [visibleold] BIT NOT NULL DEFAULT 1,
    [groupmode] INT NOT NULL DEFAULT 0,
    [groupingid] INT NOT NULL DEFAULT 0,
    [completion] INT NOT NULL DEFAULT 0,
    [completiongradeitemnumber] INT NULL,
    [completionview] BIT NOT NULL DEFAULT 0,
    [completionexpected] DATETIME2 NULL,
    [availability] NVARCHAR(MAX) NULL,
    [showdescription] BIT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_course_modules] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_role] (
    [id] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(255) NOT NULL,
    [shortname] NVARCHAR(255) NOT NULL,
    [description] NVARCHAR(MAX) NULL,
    [sortorder] INT NOT NULL,
    [archetype] NVARCHAR(255) NULL,
    CONSTRAINT [PK_mdl_role] PRIMARY KEY ([id]),
    CONSTRAINT [UK_mdl_role_shortname] UNIQUE ([shortname])
);

-- CreateTable
CREATE TABLE [mdl_role_assignments] (
    [id] INT NOT NULL IDENTITY(1,1),
    [roleid] INT NOT NULL,
    [contextid] INT NOT NULL,
    [userid] INT NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    [modifierid] INT NOT NULL,
    [component] NVARCHAR(255) NULL,
    [itemid] INT NOT NULL DEFAULT 0,
    [sortorder] INT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_role_assignments] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_user_enrolments] (
    [id] INT NOT NULL IDENTITY(1,1),
    [enrolid] INT NOT NULL,
    [userid] INT NOT NULL,
    [courseid] INT NOT NULL,
    [status] INT NOT NULL DEFAULT 0,
    [timestart] DATETIME2 NULL,
    [timeend] DATETIME2 NULL,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_user_enrolments] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_assign] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [name] NVARCHAR(255) NOT NULL,
    [intro] NVARCHAR(MAX) NOT NULL,
    [introformat] INT NOT NULL DEFAULT 0,
    [alwaysshowdescription] BIT NOT NULL DEFAULT 1,
    [nosubmissions] BIT NOT NULL DEFAULT 0,
    [submissiondrafts] BIT NOT NULL DEFAULT 0,
    [sendnotifications] BIT NOT NULL DEFAULT 0,
    [sendlatenotifications] BIT NOT NULL DEFAULT 0,
    [duedate] DATETIME2 NULL,
    [allowsubmissionsfromdate] DATETIME2 NULL,
    [grade] INT NULL,
    [timemodified] DATETIME2 NOT NULL,
    [requiresubmissionstatement] BIT NOT NULL DEFAULT 0,
    [completionsubmit] BIT NOT NULL DEFAULT 0,
    [cutoffdate] DATETIME2 NULL,
    [gradingduedate] DATETIME2 NULL,
    [teamsubmission] BIT NOT NULL DEFAULT 0,
    [requireallteammemberssubmit] BIT NOT NULL DEFAULT 0,
    [teamsubmissiongroupingid] INT NOT NULL DEFAULT 0,
    [blindmarking] BIT NOT NULL DEFAULT 0,
    [revealidentities] BIT NOT NULL DEFAULT 0,
    [attemptreopenmethod] NVARCHAR(255) NOT NULL DEFAULT 'none',
    [maxattempts] INT NOT NULL DEFAULT (-1),
    [markingworkflow] BIT NOT NULL DEFAULT 0,
    [markingallocation] BIT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_assign] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_assign_submission] (
    [id] INT NOT NULL IDENTITY(1,1),
    [assignment] INT NOT NULL,
    [userid] INT NOT NULL,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    [status] NVARCHAR(255) NOT NULL,
    [groupid] INT NOT NULL DEFAULT 0,
    [attemptnumber] INT NOT NULL DEFAULT 0,
    [latest] BIT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_assign_submission] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_quiz] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [name] NVARCHAR(255) NOT NULL,
    [intro] NVARCHAR(MAX) NOT NULL,
    [introformat] INT NOT NULL DEFAULT 0,
    [timeopen] DATETIME2 NULL,
    [timeclose] DATETIME2 NULL,
    [timelimit] INT NULL,
    [preferredbehaviour] NVARCHAR(255) NOT NULL,
    [attempts] INT NOT NULL DEFAULT 0,
    [grademethod] INT NOT NULL DEFAULT 1,
    [decimalpoints] INT NOT NULL DEFAULT 2,
    [questiondecimalpoints] INT NOT NULL DEFAULT (-1),
    [sumgrades] INT NOT NULL DEFAULT 0,
    [grade] INT NOT NULL DEFAULT 0,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    [password] NVARCHAR(255) NULL,
    [subnet] NVARCHAR(255) NULL,
    [browsersecurity] NVARCHAR(255) NULL,
    [delay1] INT NOT NULL DEFAULT 0,
    [delay2] INT NOT NULL DEFAULT 0,
    [showuserpicture] INT NOT NULL DEFAULT 0,
    [showblocks] INT NOT NULL DEFAULT 0,
    [navmethod] NVARCHAR(255) NOT NULL DEFAULT 'free',
    [shuffleanswers] INT NOT NULL DEFAULT 1,
    CONSTRAINT [PK_mdl_quiz] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_course_completions] (
    [id] INT NOT NULL IDENTITY(1,1),
    [userid] INT NOT NULL,
    [course] INT NOT NULL,
    [timeenrolled] DATETIME2 NOT NULL,
    [timestarted] DATETIME2 NOT NULL,
    [timecompleted] DATETIME2 NULL,
    [reaggregate] DATETIME2 NULL,
    CONSTRAINT [PK_mdl_course_completions] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_forum] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [type] NVARCHAR(255) NOT NULL DEFAULT 'general',
    [name] NVARCHAR(255) NOT NULL,
    [intro] NVARCHAR(MAX) NOT NULL,
    [introformat] INT NOT NULL DEFAULT 0,
    [assessed] INT NOT NULL DEFAULT 0,
    [assesstimestart] DATETIME2 NULL,
    [assesstimefinish] DATETIME2 NULL,
    [scale] INT NOT NULL DEFAULT 0,
    [maxbytes] INT NOT NULL DEFAULT 0,
    [maxattachments] INT NOT NULL DEFAULT 1,
    [forcesubscribe] INT NOT NULL DEFAULT 0,
    [trackingtype] INT NOT NULL DEFAULT 1,
    [rsstype] INT NOT NULL DEFAULT 0,
    [rssarticles] INT NOT NULL DEFAULT 0,
    [timemodified] DATETIME2 NOT NULL,
    [warnafter] INT NOT NULL DEFAULT 0,
    [blockafter] INT NOT NULL DEFAULT 0,
    [blockperiod] INT NOT NULL DEFAULT 0,
    [completiondiscussions] INT NOT NULL DEFAULT 0,
    [completionreplies] INT NOT NULL DEFAULT 0,
    [completionposts] INT NOT NULL DEFAULT 0,
    [displaywordcount] BIT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_forum] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_forum_discussions] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [forum] INT NOT NULL,
    [name] NVARCHAR(255) NOT NULL,
    [firstpost] INT NOT NULL,
    [userid] INT NOT NULL,
    [groupid] INT NOT NULL DEFAULT (-1),
    [assessed] BIT NOT NULL DEFAULT 1,
    [timemodified] DATETIME2 NOT NULL,
    [usermodified] INT NOT NULL DEFAULT 0,
    [timestart] DATETIME2 NULL,
    [timeend] DATETIME2 NULL,
    [pinned] BIT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_forum_discussions] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_forum_posts] (
    [id] INT NOT NULL IDENTITY(1,1),
    [discussion] INT NOT NULL,
    [parent] INT NOT NULL DEFAULT 0,
    [userid] INT NOT NULL,
    [created] DATETIME2 NOT NULL,
    [modified] DATETIME2 NOT NULL,
    [mailed] INT NOT NULL DEFAULT 0,
    [subject] NVARCHAR(255) NOT NULL,
    [message] NVARCHAR(MAX) NOT NULL,
    [messageformat] INT NOT NULL DEFAULT 0,
    [messagetrust] INT NOT NULL DEFAULT 0,
    [attachment] NVARCHAR(255) NULL,
    [totalscore] INT NOT NULL DEFAULT 0,
    [mailnow] INT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_forum_posts] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_grade_items] (
    [id] INT NOT NULL IDENTITY(1,1),
    [courseid] INT NOT NULL,
    [categoryid] INT NULL,
    [itemname] NVARCHAR(255) NULL,
    [itemtype] NVARCHAR(255) NOT NULL,
    [itemmodule] NVARCHAR(255) NULL,
    [iteminstance] INT NULL,
    [itemnumber] INT NULL,
    [iteminfo] NVARCHAR(MAX) NULL,
    [idnumber] NVARCHAR(255) NULL,
    [calculation] NVARCHAR(MAX) NULL,
    [gradetype] INT NOT NULL DEFAULT 1,
    [grademax] DECIMAL(10,5) NOT NULL DEFAULT 100.00000,
    [grademin] DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    [scaleid] INT NULL,
    [outcomeid] INT NULL,
    [gradepass] DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    [multfactor] DECIMAL(10,5) NOT NULL DEFAULT 1.00000,
    [plusfactor] DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    [aggregationcoef] DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    [aggregationcoef2] DECIMAL(10,5) NOT NULL DEFAULT 0.00000,
    [sortorder] INT NOT NULL DEFAULT 0,
    [display] INT NOT NULL DEFAULT 0,
    [decimals] INT NULL,
    [hidden] INT NOT NULL DEFAULT 0,
    [locked] INT NOT NULL DEFAULT 0,
    [locktime] DATETIME2 NULL,
    [needsupdate] INT NOT NULL DEFAULT 0,
    [weightoverride] INT NOT NULL DEFAULT 0,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_grade_items] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_grade_grades] (
    [id] INT NOT NULL IDENTITY(1,1),
    [itemid] INT NOT NULL,
    [userid] INT NOT NULL,
    [rawgrade] INT NULL,
    [rawgrademax] INT NOT NULL DEFAULT 100,
    [rawgrademin] INT NOT NULL DEFAULT 0,
    [finalgrade] INT NULL,
    [hidden] INT NOT NULL DEFAULT 0,
    [locked] INT NOT NULL DEFAULT 0,
    [locktime] DATETIME2 NULL,
    [exported] INT NOT NULL DEFAULT 0,
    [overridden] INT NOT NULL DEFAULT 0,
    [excluded] INT NOT NULL DEFAULT 0,
    [feedback] NVARCHAR(MAX) NULL,
    [feedbackformat] INT NOT NULL DEFAULT 0,
    [information] NVARCHAR(MAX) NULL,
    [informationformat] INT NOT NULL DEFAULT 0,
    [timecreated] DATETIME2 NOT NULL,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_grade_grades] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_resource] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [name] NVARCHAR(255) NOT NULL,
    [intro] NVARCHAR(MAX) NULL,
    [introformat] INT NOT NULL DEFAULT 0,
    [tobemigrated] INT NOT NULL DEFAULT 0,
    [legacyfiles] INT NOT NULL DEFAULT 0,
    [legacyfileslast] INT NULL,
    [display] INT NOT NULL DEFAULT 0,
    [displayoptions] NVARCHAR(MAX) NULL,
    [filterfiles] INT NOT NULL DEFAULT 0,
    [revision] INT NOT NULL DEFAULT 0,
    [timemodified] DATETIME2 NOT NULL,
    CONSTRAINT [PK_mdl_resource] PRIMARY KEY ([id])
);

-- CreateTable
CREATE TABLE [mdl_scorm] (
    [id] INT NOT NULL IDENTITY(1,1),
    [course] INT NOT NULL,
    [name] NVARCHAR(255) NOT NULL,
    [scormtype] NVARCHAR(255) NOT NULL DEFAULT 'local',
    [reference] NVARCHAR(255) NOT NULL,
    [intro] NVARCHAR(MAX) NOT NULL,
    [introformat] INT NOT NULL DEFAULT 0,
    [version] NVARCHAR(255) NOT NULL,
    [maxgrade] INT NOT NULL DEFAULT 0,
    [grademethod] INT NOT NULL DEFAULT 0,
    [whatgrade] INT NOT NULL DEFAULT 0,
    [maxattempt] INT NOT NULL DEFAULT 1,
    [forcecompleted] BIT NOT NULL DEFAULT 0,
    [forcenewattempt] INT NOT NULL DEFAULT 0,
    [lastattemptlock] BIT NOT NULL DEFAULT 0,
    [masteryoverride] BIT NOT NULL DEFAULT 1,
    [displayattemptstatus] INT NOT NULL DEFAULT 1,
    [displaycoursestructure] BIT NOT NULL DEFAULT 0,
    [updatefreq] INT NOT NULL DEFAULT 0,
    [sha1hash] NVARCHAR(255) NULL,
    [md5hash] NVARCHAR(255) NULL,
    [revision] INT NOT NULL DEFAULT 0,
    [launch] INT NOT NULL DEFAULT 0,
    [skipview] INT NOT NULL DEFAULT 1,
    [hidebrowse] BIT NOT NULL DEFAULT 0,
    [hidetoc] INT NOT NULL DEFAULT 0,
    [nav] INT NOT NULL DEFAULT 1,
    [navpositionleft] INT NULL,
    [navpositiontop] INT NULL,
    [auto] BIT NOT NULL DEFAULT 0,
    [popup] BIT NOT NULL DEFAULT 0,
    [width] INT NOT NULL DEFAULT 100,
    [height] INT NOT NULL DEFAULT 600,
    [timeopen] DATETIME2 NULL,
    [timeclose] DATETIME2 NULL,
    [timemodified] DATETIME2 NOT NULL,
    [completionstatusrequired] INT NULL,
    [completionscorerequired] INT NULL,
    [completionstatusallscos] INT NULL,
    [autocommit] BIT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_mdl_scorm] PRIMARY KEY ([id])
);

-- Create table for userrole
CREATE TABLE [mdl_userrole] (
    [id] INT NOT NULL IDENTITY(1,1),
    [userid] INT NOT NULL,
    [roleid] INT NOT NULL,
    [timemodified] DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_mdl_userrole] PRIMARY KEY ([id])
);

-- AddForeignKey
ALTER TABLE [mdl_course_category_map] ADD CONSTRAINT [FK_mdl_course_category_map_category] FOREIGN KEY ([category]) REFERENCES [mdl_course_categories]([id]);

-- AddForeignKey
ALTER TABLE [mdl_course_category_map] ADD CONSTRAINT [FK_mdl_course_category_map_course] FOREIGN KEY ([course]) REFERENCES [mdl_course]([id]);

-- AddForeignKey
ALTER TABLE [mdl_course_sections] ADD CONSTRAINT [FK_mdl_course_sections_course] FOREIGN KEY ([course]) REFERENCES [mdl_course]([id]);

-- AddForeignKey
ALTER TABLE [mdl_course_modules] ADD CONSTRAINT [FK_mdl_course_modules_course] FOREIGN KEY ([course]) REFERENCES [mdl_course]([id]);

-- AddForeignKey
ALTER TABLE [mdl_course_modules] ADD CONSTRAINT [FK_mdl_course_modules_module] FOREIGN KEY ([module]) REFERENCES [mdl_modules]([id]);

-- AddForeignKey
ALTER TABLE [mdl_role_assignments] ADD CONSTRAINT [FK_mdl_role_assignments_roleid] FOREIGN KEY ([roleid]) REFERENCES [mdl_role]([id]);

-- AddForeignKey
ALTER TABLE [mdl_role_assignments] ADD CONSTRAINT [FK_mdl_role_assignments_userid] FOREIGN KEY ([userid]) REFERENCES [mdl_user]([id]);

-- AddForeignKey
ALTER TABLE [mdl_user_enrolments] ADD CONSTRAINT [FK_mdl_user_enrolments_userid] FOREIGN KEY ([userid]) REFERENCES [mdl_user]([id]);

-- AddForeignKey
ALTER TABLE [mdl_user_enrolments] ADD CONSTRAINT [FK_mdl_user_enrolments_courseid] FOREIGN KEY ([courseid]) REFERENCES [mdl_course]([id]);

-- AddForeignKey
ALTER TABLE [mdl_assign_submission] ADD CONSTRAINT [FK_mdl_assign_submission_assignment] FOREIGN KEY ([assignment]) REFERENCES [mdl_assign]([id]);

-- AddForeignKey
ALTER TABLE [mdl_assign_submission] ADD CONSTRAINT [FK_mdl_assign_submission_userid] FOREIGN KEY ([userid]) REFERENCES [mdl_user]([id]);

-- AddForeignKey
ALTER TABLE [mdl_course_completions] ADD CONSTRAINT [FK_mdl_course_completions_userid] FOREIGN KEY ([userid]) REFERENCES [mdl_user]([id]);

-- AddForeignKey
ALTER TABLE [mdl_course_completions] ADD CONSTRAINT [FK_mdl_course_completions_course] FOREIGN KEY ([course]) REFERENCES [mdl_course]([id]);

-- AddForeignKey
ALTER TABLE [mdl_forum_discussions] ADD CONSTRAINT [FK_mdl_forum_discussions_forum] FOREIGN KEY ([forum]) REFERENCES [mdl_forum]([id]);

-- AddForeignKey
ALTER TABLE [mdl_forum_posts] ADD CONSTRAINT [FK_mdl_forum_posts_discussion] FOREIGN KEY ([discussion]) REFERENCES [mdl_forum_discussions]([id]);

-- AddForeignKey
ALTER TABLE [mdl_grade_grades] ADD CONSTRAINT [FK_mdl_grade_grades_itemid] FOREIGN KEY ([itemid]) REFERENCES [mdl_grade_items]([id]);

-- AddForeignKey
ALTER TABLE [mdl_userrole] ADD CONSTRAINT [FK_mdl_userrole_userid] FOREIGN KEY ([userid]) REFERENCES [mdl_user]([id]);

-- AddForeignKey
ALTER TABLE [mdl_userrole] ADD CONSTRAINT [FK_mdl_userrole_roleid] FOREIGN KEY ([roleid]) REFERENCES [mdl_role]([id]);
