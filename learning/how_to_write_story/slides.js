const slidesData = [
    {
        id: "title",
        layout: "title",
        title: "Your Story Starts Here",
        subtitle: "A Modern, AI-Powered Writing Workflow for Sarah",
        background: "linear-gradient(135deg, #F0F4F8 0%, #E6E9EF 100%)"
    },
    {
        id: "github-intro",
        layout: "concept",
        title: "Why GitHub for Stories?",
        bullets: [
            "**Time Machine**: Every version of your story is saved. Never lose a draft.",
            "**Collaboration**: Easily share and review changes with others.",
            "**Transparency**: See exactly what changed between Chapters 1 and 2.",
            "**Cloud Backup**: Your work is safe, even if your computer isn't."
        ]
    },
    {
        id: "case-study-loney",
        layout: "concept",
        title: "Case Study: 'loney_coder'",
        bullets: [
            "**Theme**: A meta-story about a coder's emotional life.",
            "**Structure**: Chapter-based files like `第03章_版本控制的失恋.md`.",
            "**Insight**: Notice how the project uses Chinese filenames for accessibility while keeping a clean structure.",
            "**Action**: We will use this to practice 'Pulling' today."
        ]
    },
    {
        id: "case-study-rejection",
        layout: "concept",
        title: "Case Study: 'last_rejection'",
        bullets: [
            "**Theme**: High-quality, literary fiction.",
            "**Structure**: 20+ chapters in English, showing long-term project management.",
            "**Insight**: A perfect example of maintaining atmospheric consistency over thousands of words.",
            "**Workflow**: Iterative refinement through the 'Score' system."
        ]
    },
    {
        id: "github-concepts",
        layout: "concept",
        title: "The 4 Pillars of Git",
        bullets: [
            "**Branch**: Your private sandbox (e.g., `sarah/new-book`).",
            "**Commit**: Taking a 'snapshot' of your progress.",
            "**Push**: Uploading your snapshots to the cloud.",
            "**Pull**: Getting the latest updates from the team."
        ]
    },
    {
        id: "antigravity-intro",
        layout: "concept",
        title: "Meet Antigravity",
        bullets: [
            "**Your 24/7 Co-Author**: An AI assistant that knows your project.",
            "**Context Aware**: It reads your previous chapters and style guides.",
            "**Multimodal**: Ask it to brainstorm, write, or critique.",
            "**Interface**: Chat-based interaction with powerful workspace tools."
        ]
    },
    {
        id: "exercise-branch-management",
        layout: "interactive",
        title: "Detailed Exercise: Branch Switching",
        instructions: "Imagine you are helping polish 'loney_coder'. You need to switch to that context.",
        task: "In your terminal, run: `git checkout loney_coder` (if the branch exists) or observe the branch list.",
        hint: "Branches keep 'loney_coder' and 'last_rejection' work completely separate and safe."
    },
    {
        id: "quickstart-workflow",
        layout: "concept",
        title: "The 'Quickstart' Philosophy",
        bullets: [
            "**Standardization**: Every story follows the same folder structure.",
            "**Flow**: Draft -> Score -> Refine -> Publish.",
            "**Publishing**: Single-command publishing to the public `main` branch.",
            "**Focus**: Spend more time writing, less time managing files."
        ]
    },
    {
        id: "the-edit-cycle",
        layout: "concept",
        title: "The Edit Cycle (Inside `tmp/`)",
        bullets: [
            "1. **current.txt**: Put your active scene or chapter here.",
            "2. **Ask for Score**: Let Antigravity evaluate the text.",
            "3. **Refine**: Fix issues based on the feedback.",
            "4. **Done**: Snapshot your chapter and move to the next."
        ]
    },
    {
        id: "scoring-criteria",
        layout: "concept",
        title: "The 4 Pillars of Quality",
        bullets: [
            "**Narrative (20%)**: Does the plot flow logically?",
            "**Character (20%)**: Are the emotions and inner thoughts deep?",
            "**Aesthetics (30%)**: Is the writing 'showing' rather than 'telling'?",
            "**Theme (30%)**: Is the 'Will to Atrophy' or philosophical core present?"
        ]
    },
    {
        id: "exercise-edit-draft",
        layout: "interactive",
        title: "Detailed Exercise: Draft Refinement",
        instructions: "Open 'last_rejection/chapter_01.md'. Copy a few sentences into a new `tmp/sarah/current.txt`.",
        task: "Change the tone. If it's cold, make it warm. If it's bright, make it dark.",
        hint: "Use Antigravity to help: 'Rewrite this paragraph to be more melancholic'."
    },
    {
        id: "exercise-iterative-score",
        layout: "interactive",
        title: "Detailed Exercise: The Scoring Loop",
        instructions: "Now that you've edited your `current.txt`, let's see how Antigravity likes it.",
        task: "Type 'Score my current.txt' and read the feedback for 'Aesthetics'.",
        hint: "Look for 'Show vs Tell' advice. This is where stories become literature."
    },
    {
        id: "publishing-flow",
        layout: "code",
        title: "The 'Publishing' Magic",
        code: `Publish story loney_coder`,
        description: "This command merges your validated draft from your working branch into the public 'main' branch automatically."
    },
    {
        id: "ai-dialogue-art",
        layout: "concept",
        title: "The Art of AI Dialogue",
        bullets: [
            "**Be Specific**: Instead of 'Make it better', say 'Make the dialogue more tense and use shorter sentences'.",
            "**Stylistic Guidance**: 'Rewrite this in the style of a 1940s noir novel'.",
            "**Logic Checks**: 'Does it make sense that the protagonist would leave the door unlocked here?'",
            "**World Building**: 'Brainstorm 5 sensory details for a futuristic market that smells of ozone and spices'."
        ]
    },
    {
        id: "memory-gap",
        layout: "concept",
        title: "Managing the 'Memory Gap'",
        bullets: [
            "**The AI Forgets**: Large conversations can make the AI lose track of details from Slide 1.",
            "**Summarize & Remind**: Periodically say, 'Reminder: Sarah is a cynical detective who hates coffee'.",
            "**One Task at a Time**: Don't ask for a plot outline and a chapter edit in the same breath.",
            "**Context is King**: If starting a new session, paste the last summary of your story."
        ]
    },
    {
        id: "exercise-context-reminder",
        layout: "interactive",
        title: "Exercise: The Context Bridge",
        instructions: "Imagine you've been chatting with Antigravity for 2 hours. It might have forgotten your character's motivation.",
        task: "Draft a 'Context Reminder' message: 'We are writing a scene for last_rejection. Remember, the tone is cold and the theme is voluntary atrophy.'",
        hint: "Doing this every 20-30 messages keeps the AI aligned with your vision."
    },
    {
        id: "discussion",
        layout: "concept",
        title: "Building a Rhythm",
        bullets: [
            "**Consistency vs. perfection**: Better to commit daily than wait for a month.",
            "**The Feedback Loop**: Use AI critiques as a mirror, not a replacement.",
            "**Release Strategy**: Start small, build a 'Series' profile.",
            "**Next Step**: Finish Chapter 1 by Friday?"
        ]
    },
    {
        id: "conclusion",
        layout: "title",
        title: "Write with Purpose.",
        subtitle: "The world is waiting for your story.",
        background: "linear-gradient(135deg, #E6E9EF 0%, #F0F4F8 100%)"
    }
];

export default slidesData;
