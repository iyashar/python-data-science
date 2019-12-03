from app import app, render_template, pd, np, plt, sns, Axes3D, PCA, preprocessing



@app.route('/')
def index():
    csvNames = ['titanic', 'melb', 'airbase', 'flow']
    return render_template('index.html', csvNames=csvNames)



@app.route('/show/<name>')
def csvViewer(name):
    csvNames= ['titanic', 'melb', 'airbase', 'flow']
    name = name.lower()
    if name in csvNames:

        path = './app/static/data/{}.csv'.format(name)
        df   = pd.read_csv(path)
        records = df.head()

        pcaImages = []
        if name == 'titanic':
            session4(df)
            pcaImages = session5(df)


        return render_template('show.html', records=records , name=name, pcaImages=pcaImages)

    else:
        code = 404
        return render_template('error.html', code=code)



def session4(df):
    df = df[df['Age'].notnull()]
    Age = df.Age

    # plt.ioff()
    # fig, ax = plt.subplots()
    fig = plt.figure(figsize=(7,6), dpi=55)
    Age.plot.kde()
    Age.plot.hist(normed=True, title="Titanic mix plot!")
    plt.savefig("./app/static/tmp/titanic_mix.png")
    plt.close(fig) 
    # --
    fig = plt.figure(figsize=(7,6), dpi=55)
    Age.plot.hist(title="Titanic Age hist")
    fig.savefig("./app/static/tmp/titanic_hist.png")
    plt.close(fig) 
    # --
    fig = plt.figure(figsize=(7,6), dpi=55)
    Age.plot.kde(title="Titanic Age kde")
    fig.savefig("./app/static/tmp/titanic_kde.png")
    plt.close(fig) 



def session5(df):
    ### Preprocessing

    ## Engineer Features ##
    # Aside from 'Sex', the 'Age' feature is second in importance. To avoid overfitting, group people into logical human age groups.
    # Each 'Cabin' starts with a letter. Probably, this letter is more important than the number that follows, so slice it off.
    # 'Fare' is another continuous value that should be simplified, placing the values into quartile bins accordingly.
    # Extract information from the 'Name' feature. Rather than use the full name, extract the last name and prefix and then append them as their own features.
    # Lastly, drop useless features ('Ticket', 'Name', and 'Embarked').

    session5_df = transform_features(df)

    ## Encode Data ##
    # Normalize and transform categorical non-numerical features to numerical with the LabelEncoder tool from scikit-learn,
    # making out data more flexible for various algorithms.
    session5_df = encode_features(session5_df)



    # # normalize data
    # scaled_data = pd.DataFrame(preprocessing.scale(session5_df),columns = session5_df.columns) 

    # # PCA
    # pca = PCA(n_components=2)
    # x_pca = pca.fit_transform(scaled_data)



    ### PCA ###
    
    # normalize data
    scaler = preprocessing.StandardScaler()
    scaler.fit(session5_df)

    preprocessing.StandardScaler(copy=True, with_mean=True, with_std=True)
    scaled_data = scaler.transform(session5_df)

    # PCA
    pca = PCA(n_components=3)
    pca.fit(scaled_data)

    x_pca = pca.transform(scaled_data)

    X = x_pca[:,0]
    Y = x_pca[:,1]
    Z = x_pca[:,2]

    # # scaled_data.shape
    # # x_pca.shape

    features = ['PassengerId', 'Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Cabin']

    pcaImages = []
    for feature in features:
        fig = plt.figure(figsize=(6,4), dpi=95)

        ax = Axes3D(fig)
        p = ax.scatter(X, Y, Z, c=session5_df[f"{feature}"], marker='o') 

        # plt.scatter(x, y, c=session5_df[f"{feature}"], cmap='plasma') #,edgecolor='none', alpha=0.5
        plt.title(f"{feature}")
        # plt.xlabel('PC-1')
        # plt.ylabel('PC-2')

        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')

        plt.colorbar(p) 
        imgName = f'PCA__{feature}.png'
        pcaImages.append(imgName)
        fig.savefig(f"./app/static/tmp/{imgName}", bbox_inches='tight')
        plt.close(fig) 


    ### Interpreting the components ###
    df_comp = pd.DataFrame(pca.components_, columns=features, index = ['PC-1 (X)','PC-2 (Y)', 'PC-3 (Z)' ])
    figX = plt.figure(figsize=(12,6))
    sns.heatmap(df_comp,cmap='plasma',)
    plt.title("Interpreting the components ")
    figX.savefig(f"./app/static/tmp/PCA__heatmap__.png")

    pcaImages.append('PCA__heatmap__.png')
    return pcaImages



# Code adapted from https://www.kaggle.com/jeffd23/scikit-learn-ml-from-start-to-finish
def simplify_ages(df):
    df.Age = df.Age.fillna(-0.5)
    bins = (-1, 0, 5, 12, 18, 25, 35, 60, 120)
    group_names = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
    categories = pd.cut(df.Age, bins, labels=group_names)
    df.Age = categories
    return df

def simplify_cabins(df):
    df.Cabin = df.Cabin.fillna('N')
    df.Cabin = df.Cabin.apply(lambda x: x[0])
    return df

def simplify_fares(df):
    df.Fare = df.Fare.fillna(-0.5)
    bins = (-1, 0, 8, 15, 31, 1000)
    group_names = ['Unknown', '1_quartile', '2_quartile', '3_quartile', '4_quartile']
    categories = pd.cut(df.Fare, bins, labels=group_names)
    df.Fare = categories
    return df 
    
def drop_features(df):
    return df.drop(['Ticket', 'Name', 'Embarked'], axis=1)

def transform_features(df):
    df = simplify_ages(df)
    df = simplify_cabins(df)
    df = simplify_fares(df)
    df = drop_features(df)
    return df

# ###
def encode_features(df):
    features = ['Fare', 'Cabin', 'Age', 'Sex']
    
    for feature in features:
        le = preprocessing.LabelEncoder()
        le = le.fit(df[feature])
        df[feature] = le.transform(df[feature])
    return df

