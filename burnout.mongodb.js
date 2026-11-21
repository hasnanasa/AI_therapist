use("psych_support")

const burnout = [
  { _id: "bur_001", phrase: "I'm exhausted", signal: "fatigue", variants: ["I'm so tired", "I'm drained", "I have no energy"], intensity_modifiers: ["always", "constantly", "every day"], negation_sensitive: true, weights: { burnout: 0.95, rumination: 0.20 } },
  { _id: "bur_002", phrase: "I can't keep going", signal: "fatigue", variants: ["I can't continue", "I can't do this anymore"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.95, self_criticism: 0.25 } },
  { _id: "bur_003", phrase: "I'm running on empty", signal: "fatigue", variants: ["I have nothing left", "I'm running on fumes"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_004", phrase: "I wake up tired", signal: "fatigue", variants: ["I don't feel rested", "I never feel refreshed"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_005", phrase: "everything feels heavy", signal: "fatigue", variants: ["everything is a burden", "everything is hard"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_006", phrase: "I have no motivation", signal: "no_motivation", variants: ["I can't motivate myself", "I don't want to do anything"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90, procrastination: 0.50 } },
  { _id: "bur_007", phrase: "I don't care anymore", signal: "no_motivation", variants: ["nothing matters", "I've stopped caring"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_008", phrase: "I can't get excited about anything", signal: "no_motivation", variants: ["nothing brings me joy", "I feel flat"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_009", phrase: "small tasks feel impossible", signal: "no_motivation", variants: ["even easy things are hard", "simple tasks wear me out"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90, procrastination: 0.45 } },
  { _id: "bur_010", phrase: "getting out of bed is hard", signal: "no_motivation", variants: ["I can't get up", "staying in bed is easier"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.85 } },

  { _id: "bur_011", phrase: "I'm emotionally drained", signal: "emotional_drain", variants: ["I feel empty inside", "I have no feelings left"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_012", phrase: "I can't handle one more thing", signal: "emotional_drain", variants: ["I'm at my limit", "I'll snap"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_013", phrase: "I feel numb", signal: "emotional_drain", variants: ["I feel nothing", "I'm disconnected from my feelings"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_014", phrase: "I'm on edge all the time", signal: "emotional_drain", variants: ["I snap easily", "I'm irritable"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_015", phrase: "I cry over small things", signal: "emotional_drain", variants: ["I tear up easily", "little things set me off"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },

  { _id: "bur_016", phrase: "I dread work", signal: "work_dread", variants: ["I can't face work", "work drains me"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_017", phrase: "I can't focus at work", signal: "work_dread", variants: ["I zone out at work", "I can't concentrate"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80, rumination: 0.30 } },
  { _id: "bur_018", phrase: "I'm doing the minimum", signal: "work_dread", variants: ["I do the bare minimum", "I just go through the motions"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_019", phrase: "I used to care about my work", signal: "work_dread", variants: ["I used to be passionate", "I used to enjoy it"], intensity_modifiers: [], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_020", phrase: "I count the hours until I can leave", signal: "work_dread", variants: ["I watch the clock", "I wait for the day to end"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },

  { _id: "bur_021", phrase: "I feel detached from everything", signal: "detachment", variants: ["I feel far away", "I'm not really here"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_022", phrase: "I'm going through the motions", signal: "detachment", variants: ["I'm on autopilot", "I'm just existing"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_023", phrase: "nothing feels real", signal: "detachment", variants: ["I feel like I'm watching my life", "it all feels foggy"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_024", phrase: "I've stopped enjoying things", signal: "detachment", variants: ["I don't enjoy anything anymore", "hobbies feel pointless"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_025", phrase: "I feel empty", signal: "detachment", variants: ["there's nothing inside", "I'm hollow"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },

  { _id: "bur_026", phrase: "I can't sleep", signal: "sleep_problems", variants: ["I struggle to sleep", "I lie awake"], intensity_modifiers: ["always", "every night"], negation_sensitive: true, weights: { burnout: 0.80, rumination: 0.50 } },
  { _id: "bur_027", phrase: "I sleep too much", signal: "sleep_problems", variants: ["I oversleep", "I sleep all day"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_028", phrase: "I never feel rested", signal: "sleep_problems", variants: ["sleep doesn't help", "I wake up exhausted"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },

  { _id: "bur_029", phrase: "I get sick all the time", signal: "physical", variants: ["I'm always catching colds", "my body is falling apart"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_030", phrase: "I have headaches constantly", signal: "physical", variants: ["my head hurts all the time", "constant headaches"], intensity_modifiers: ["always", "constantly"], negation_sensitive: true, weights: { burnout: 0.75 } },
  { _id: "bur_031", phrase: "my body aches", signal: "physical", variants: ["everything hurts", "I'm sore all over"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },
  { _id: "bur_032", phrase: "I have no appetite", signal: "physical", variants: ["I forget to eat", "food doesn't interest me"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },

  { _id: "bur_033", phrase: "I don't see the point anymore", signal: "hopelessness", variants: ["what's the point", "nothing matters"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85, self_criticism: 0.45 } },
  { _id: "bur_034", phrase: "I used to be different", signal: "identity_loss", variants: ["I don't recognize myself", "I've changed"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_035", phrase: "I don't know who I am anymore", signal: "identity_loss", variants: ["I've lost myself", "I don't know what I want"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_036", phrase: "I've lost interest in my friends", signal: "withdrawal", variants: ["I don't want to see anyone", "I cancel on people"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80, avoidance: 0.55 } },
  { _id: "bur_037", phrase: "I just want to be left alone", signal: "withdrawal", variants: ["I want to disappear", "I need everyone to leave me alone"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80, avoidance: 0.65 } },
  { _id: "bur_038", phrase: "I can't handle socializing", signal: "withdrawal", variants: ["people drain me", "I have no energy for people"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80, avoidance: 0.50 } },

  { _id: "bur_039", phrase: "I can't remember the last time I felt okay", signal: "chronicity", variants: ["I don't remember feeling good", "it's been so long"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_040", phrase: "I feel like I'm breaking down", signal: "chronicity", variants: ["I'm falling apart", "I'm at the breaking point"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  // ── 41–50: Physical depletion ──
  { _id: "bur_041", phrase: "my body feels heavy", signal: "physical", variants: ["everything feels heavy", "my limbs feel like lead"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_042", phrase: "I feel physically drained", signal: "physical", variants: ["my body is drained", "I have no physical energy"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_043", phrase: "I can barely get through the day", signal: "fatigue", variants: ["I struggle to get through the day", "the day feels endless"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_044", phrase: "I wake up already tired", signal: "fatigue", variants: ["I wake up exhausted", "mornings are the hardest"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_045", phrase: "I sleep but don't feel rested", signal: "sleep_problems", variants: ["sleep doesn't help", "I never feel refreshed"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_046", phrase: "my eyes feel tired all the time", signal: "physical", variants: ["I have tired eyes", "my body shows the exhaustion"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },
  { _id: "bur_047", phrase: "I get tired doing simple things", signal: "fatigue", variants: ["small tasks exhaust me", "even easy things tire me"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90, procrastination: 0.40 } },
  { _id: "bur_048", phrase: "I feel weak", signal: "physical", variants: ["I feel physically weak", "my strength is gone"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_049", phrase: "I've been sick more often", signal: "physical", variants: ["I keep getting sick", "my immune system is shot"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },
  { _id: "bur_050", phrase: "I have tension in my body", signal: "physical", variants: ["my body is tense", "I'm always tense"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.70 } },

  // ── 51–60: Mental fog & concentration ──
  { _id: "bur_051", phrase: "I can't concentrate", signal: "mental_fog", variants: ["my focus is gone", "I can't pay attention"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_052", phrase: "my brain feels foggy", signal: "mental_fog", variants: ["I have brain fog", "my thinking is slow"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_053", phrase: "I forget things constantly", signal: "mental_fog", variants: ["my memory is bad", "I keep forgetting"], intensity_modifiers: ["always", "constantly"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_054", phrase: "I can't think clearly", signal: "mental_fog", variants: ["my thoughts are muddy", "I can't process things"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_055", phrase: "I stare at the screen without doing anything", signal: "mental_fog", variants: ["I zone out at work", "I go blank"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_056", phrase: "even simple decisions feel hard", signal: "mental_fog", variants: ["choosing anything is exhausting", "decisions wear me out"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_057", phrase: "I lose my train of thought", signal: "mental_fog", variants: ["I forget what I was saying", "my thoughts disappear"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },
  { _id: "bur_058", phrase: "I can't read for more than a few minutes", signal: "mental_fog", variants: ["reading exhausts me", "I can't focus on text"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_059", phrase: "my mind feels slow", signal: "mental_fog", variants: ["I'm mentally slow", "my thoughts are sluggish"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80 } },
  { _id: "bur_060", phrase: "I can't do more than one thing at a time", signal: "mental_fog", variants: ["multitasking is impossible", "I can only handle one task"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75 } },

  // ── 61–70: Emotional & relational withdrawal ──
  { _id: "bur_061", phrase: "I don't enjoy anything anymore", signal: "anhedonia", variants: ["nothing brings me joy", "I've stopped enjoying things"], intensity_modifiers: ["always", "anymore"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_062", phrase: "things I used to love feel empty", signal: "anhedonia", variants: ["hobbies feel pointless", "I get nothing from what I used to love"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_063", phrase: "I've lost interest in everything", signal: "anhedonia", variants: ["nothing interests me", "I have no interests anymore"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_064", phrase: "I don't want to see anyone", signal: "withdrawal", variants: ["I avoid everyone", "I want to be alone"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80, avoidance: 0.70 } },
  { _id: "bur_065", phrase: "I can't handle talking to people", signal: "withdrawal", variants: ["socializing exhausts me", "I have no energy for people"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.80, avoidance: 0.55 } },
  { _id: "bur_066", phrase: "I cancel on everyone", signal: "withdrawal", variants: ["I cancel plans constantly", "I back out of everything"], intensity_modifiers: ["always", "constantly"], negation_sensitive: true, weights: { burnout: 0.75, avoidance: 0.75 } },
  { _id: "bur_067", phrase: "I feel detached from my loved ones", signal: "detachment", variants: ["I feel far from people I love", "I don't feel connected to anyone"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_068", phrase: "I feel like I'm watching my life from outside", signal: "detachment", variants: ["I feel like an observer", "I'm not really present"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_069", phrase: "I feel nothing", signal: "detachment", variants: ["I'm emotionally numb", "I can't feel emotions"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_070", phrase: "I'm just existing, not living", signal: "detachment", variants: ["I'm on autopilot", "I'm not really living"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },

  // ── 71–80: Work dread & hopelessness ──
  { _id: "bur_071", phrase: "the thought of work makes me sick", signal: "work_dread", variants: ["work makes me anxious", "I dread going in"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_072", phrase: "I count the minutes until I can leave", signal: "work_dread", variants: ["I watch the clock", "I wait for the day to end"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_073", phrase: "I do the minimum and go home", signal: "work_dread", variants: ["I do the bare minimum", "I coast through work"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_074", phrase: "work has taken everything from me", signal: "work_dread", variants: ["my job has drained me", "work has consumed me"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_075", phrase: "I used to care and now I don't", signal: "work_dread", variants: ["I've stopped caring about work", "I used to try harder"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_076", phrase: "nothing I do matters", signal: "hopelessness", variants: ["what I do doesn't matter", "nothing makes a difference"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85, self_criticism: 0.60 } },
  { _id: "bur_077", phrase: "what's the point of any of this", signal: "hopelessness", variants: ["what's the point", "why bother"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_078", phrase: "I can't imagine feeling better", signal: "hopelessness", variants: ["I don't see an end to this", "I can't picture things improving"], intensity_modifiers: ["always", "never"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_079", phrase: "I feel like I'm breaking", signal: "chronicity", variants: ["I'm falling apart", "I'm at my breaking point"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_080", phrase: "I can't do this anymore", signal: "chronicity", variants: ["I can't keep doing this", "I'm done"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_081", phrase: "even feeding myself feels like too much", signal: "daily_neglect", variants: ["cooking feels impossible", "I can't take care of myself"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_082", phrase: "I look fine but I'm not", signal: "masking", variants: ["I pretend I'm fine", "I hide how I feel at work"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85, self_criticism: 0.45 } },
  { _id: "bur_083", phrase: "I come home and collapse", signal: "collapse", variants: ["I crash the moment I'm home", "I don't move after work"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_084", phrase: "I sleep all day on weekends", signal: "unrefreshing_sleep", variants: ["weekends are for sleeping", "I sleep away the weekend"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_085", phrase: "I don't remember the last time I felt refreshed", signal: "unrefreshing_sleep", variants: ["I never feel rested", "refreshed doesn't happen anymore"], intensity_modifiers: ["never", "always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_086", phrase: "I haven't touched my hobbies", signal: "anhedonia", variants: ["I've abandoned my hobbies", "my hobbies are gathering dust"], intensity_modifiers: ["always", "never"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_087", phrase: "my body is giving out", signal: "physical", variants: ["my body is breaking", "my body can't take it"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_088", phrase: "I grind my teeth", signal: "physical", variants: ["I clench my jaw", "my jaw hurts from tension"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.70 } },
  { _id: "bur_089", phrase: "good things don't feel good", signal: "anhedonia", variants: ["I can't feel joy", "positive things don't register"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_090", phrase: "I can't feel anything", signal: "detachment", variants: ["I feel nothing", "my emotions are gone"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_091", phrase: "facing the day feels unbearable", signal: "morning_dread", variants: ["I can't face the day", "the day ahead terrifies me"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_092", phrase: "any small thing tips me over", signal: "emotional_drain", variants: ["I snap at small things", "little things set me off"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_093", phrase: "I do the minimum not to get fired", signal: "work_dread", variants: ["I just coast at work", "I only do what I have to"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_094", phrase: "I don't know what I enjoy anymore", signal: "identity_loss", variants: ["I've lost interest in everything", "I can't remember what I like"], intensity_modifiers: ["always", "anymore"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_095", phrase: "I don't know who I am outside of work", signal: "identity_loss", variants: ["work is all I am", "I've lost my identity"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_096", phrase: "I dread the next day", signal: "work_dread", variants: ["I spend the evening dreading tomorrow", "the weekend is a countdown to Monday"], intensity_modifiers: ["always", "every day"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_097", phrase: "I don't remember what normal feels like", signal: "chronicity", variants: ["I've forgotten what okay feels like", "I don't know what feeling good is like"], intensity_modifiers: ["always", "never"], negation_sensitive: true, weights: { burnout: 0.90 } },
  { _id: "bur_098", phrase: "I've adjusted to feeling bad", signal: "chronicity", variants: ["feeling bad is my baseline", "this is my normal now"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_099", phrase: "I have no reason to feel this way", signal: "guilt", variants: ["my life is fine on paper", "there's nothing wrong"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75, self_criticism: 0.50 } },
  { _id: "bur_100", phrase: "I wake up at 3am thinking", signal: "sleep_problems", variants: ["I wake in the middle of the night", "my sleep is broken"], intensity_modifiers: ["always", "every night"], negation_sensitive: true, weights: { burnout: 0.85, rumination: 0.65 } },
  { _id: "bur_101", phrase: "one more weekend won't fix this", signal: "chronicity", variants: ["rest doesn't help", "I keep thinking rest will fix it"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.85 } },
  { _id: "bur_102", phrase: "I don't know how to ask for help", signal: "help_seeking", variants: ["I don't know how to reach out", "I can't bring myself to ask"], intensity_modifiers: ["always"], negation_sensitive: true, weights: { burnout: 0.75, avoidance: 0.60 } }


]

const result = db.symptoms.insertMany(burnout, { ordered: false })
print("Inserted burnout:", Object.keys(result.insertedIds).length)
print("Total:", db.symptoms.countDocuments())