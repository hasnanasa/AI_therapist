"""
test_set.py — 60 labeled test sentences, 12 per problem.

These are DIFFERENT from the training examples in MongoDB.
Do NOT add these to seed_examples.txt.
"""

TEST_SET = [
    # ─── rumination (12) ───
    ("I can't stop going over what happened yesterday in my head.", "rumination"),
    ("My brain keeps replaying the same moment on a loop.", "rumination"),
    ("I keep analyzing every word I said in that meeting.", "rumination"),
    ("I lay awake last night just thinking about the same thing for hours.", "rumination"),
    ("I can't seem to switch off my thoughts no matter what I do.", "rumination"),
    ("I keep wondering what would have happened if I'd said something different.", "rumination"),
    ("My thoughts are stuck on a single topic and won't move on.", "rumination"),
    ("I overthink everything until I feel paralyzed.", "rumination"),
    ("I keep coming back to that conversation in my mind.", "rumination"),
    ("Even when I'm busy, my mind goes back to the same worry.", "rumination"),
    ("I replay my mistakes over and over and can't let them go.", "rumination"),
    ("I'm stuck in my own head again, going in circles.", "rumination"),

    # ─── procrastination (12) ───
    ("I have work to do but I keep finding other things to do instead.", "procrastination"),
    ("I told myself I'd start today and I still haven't.", "procrastination"),
    ("I keep opening the file and closing it without doing anything.", "procrastination"),
    ("Every time I think about starting, I suddenly want to clean my room.", "procrastination"),
    ("The deadline is coming and I've done nothing.", "procrastination"),
    ("I know what I need to do, I just can't get myself to do it.", "procrastination"),
    ("I keep scrolling instead of working.", "procrastination"),
    ("I put off even small tasks until they pile up.", "procrastination"),
    ("I wait until the last possible moment then panic.", "procrastination"),
    ("I make plans in my head but never act on them.", "procrastination"),
    ("I've been meaning to start this for weeks and still haven't.", "procrastination"),
    ("I always say I'll do it tomorrow, and tomorrow never comes.", "procrastination"),

    # ─── self_criticism (12) ───
    ("I feel like I'm never going to be good enough.", "self_criticism"),
    ("I hate the way I handled that situation.", "self_criticism"),
    ("Everyone else seems to have it together except me.", "self_criticism"),
    ("I always find a way to ruin things.", "self_criticism"),
    ("I'm so disappointed in myself.", "self_criticism"),
    ("I can't stop thinking about how stupid I sounded.", "self_criticism"),
    ("I don't deserve the good things that happen to me.", "self_criticism"),
    ("I feel like a fraud at work, like everyone will find out.", "self_criticism"),
    ("I'm harder on myself than I'd ever be on anyone else.", "self_criticism"),
    ("I keep beating myself up over things I can't change.", "self_criticism"),
    ("I compare myself to everyone and always come up short.", "self_criticism"),
    ("I feel worthless most days.", "self_criticism"),

    # ─── burnout (12) ───
    ("I'm running on empty and can't seem to recharge.", "burnout"),
    ("I drag myself through every day and collapse at night.", "burnout"),
    ("I used to enjoy my hobbies and now nothing interests me.", "burnout"),
    ("I feel like I've been on autopilot for months.", "burnout"),
    ("Even small tasks exhaust me.", "burnout"),
    ("I don't remember the last time I felt truly rested.", "burnout"),
    ("I'm so drained I can't think straight.", "burnout"),
    ("I feel detached from everything and everyone.", "burnout"),
    ("Work has sucked everything out of me and I have nothing left.", "burnout"),
    ("I wake up already tired, no matter how long I sleep.", "burnout"),
    ("I feel like I'm running a marathon I can't finish.", "burnout"),
    ("I just want to lie down and never get up again.", "burnout"),

    # ─── avoidance (12) ───
    ("I keep making excuses so I don't have to see anyone.", "avoidance"),
    ("I've been ignoring texts and calls for days.", "avoidance"),
    ("When something difficult comes up I just disappear.", "avoidance"),
    ("I avoid any situation that might make me uncomfortable.", "avoidance"),
    ("I pretend problems don't exist and hope they go away.", "avoidance"),
    ("I say yes to things I don't want because I can't say no.", "avoidance"),
    ("I stay home instead of going out, even when I said I would.", "avoidance"),
    ("I push difficult feelings away and don't let myself feel them.", "avoidance"),
    ("I'd rather not know than find out bad news.", "avoidance"),
    ("I cancel plans at the last minute because I can't face them.", "avoidance"),
    ("I put off making decisions for as long as possible.", "avoidance"),
    ("I stay in my comfort zone and avoid anything unfamiliar.", "avoidance"),
]