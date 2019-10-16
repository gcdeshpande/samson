from samson.prngs.dual_ec import DualEC
from samson.math.algebra.curves.named import P256
import unittest


class DualECTestCase(unittest.TestCase):
    # TODO: This is too slow to run in testing! Need better performance
    # def test_generate_backdoor(self):
    #     from samson.utilities.bytes import Bytes

    #     for num_next_bytes in range(1, 3):
    #         (P, Q, d) = DualEC.generate_backdoor(P256)
    #         dual_ec = DualEC(P, Q, Bytes.random(8).int())

    #         next_bytes = dual_ec.generate() + dual_ec.generate()[:num_next_bytes]

    #         derived_dual_ecs = DualEC.derive_from_backdoor(P, Q, d, next_bytes)
    #         expected_output  = [dual_ec.generate() for _ in range(5)]
    #         cracked_outputs  = [[possible_crack.generate() for _ in range(5)] for possible_crack in derived_dual_ecs]

    #         self.assertTrue(any([expected_output in cracked_outputs]))



    # Correctness tests manually generated using https://github.com/AntonKueltz/dual-ec-poc
    def _run_correctness_test(self, seed, e, expected_outputs):
        dual_ec = DualEC(P256.G, P256.G * e, seed)
        self.assertEqual([dual_ec.generate().int() for _ in range(len(expected_outputs))], expected_outputs)



    def test_vec0(self):
        e = 73735896533782015187601628224895778266553187375647952766676135669756673149761
        seed = 2956698742739459912
        expected_outputs = [1528308710559020308730670064423165014193853619559323950979177434848245732, 949832355581970113787088041749237407701848742159576672093362010098194979, 684958591249170713402117287346136079351181224068330515060453304941869427, 1238943362350893365517526434866018765775918677883146325061823332001931953, 1383724527967673447959171160051903773968974945809970437781173761812033163, 178160315565499975681652260774859488895451958595212168517788274171768651, 1671033994829397442926657080556753999669417747760963203670366495315063776, 24829289470163546776241441859476884338303451847915806142399346064817392, 821925075438010872390780588161595188612098032598338383356832699829993959, 1037870869607907173873376993866413231217526047169867611229467627723320699, 1262433791741521661195657095673652723031738617165559775749240632623108065, 1388081256613979345255144520589287939855769183054374436512456201675367719, 1694514306960667850711853420111836402233556762548483686345411381780477210, 474815756228014650353954939954104259481307515526196876319243403089476006, 336232157905914792245449803457056292928948272905379898958467143477275039, 1238250911635621928954574611001749995601120871104949425439063441744158558, 1634060124671606129184476065600364567465763290416133300225615138994076413, 1130389776804762639146254342863250462056150357827559183748019622816481645, 741947748098095746706934159849070783521328637490375362815767471981839907, 1678130671876333225558844356319783416491475575034408272725611833107623158, 366746825943443390306728779802211795664589276531018863261235051771023709, 224561977866534132967451354837061574329335575941142708934301819604582883, 1538773500393628121168958941893444341011364091255284612174460404159341317, 157056819336965284125195561354334486508224921402412856755984748748762991, 187531795826928619583936427113470128777582798820567455682831703001672204, 229820504155545892378344735870868474476413713855086786992428632193237938, 328665121566361194092456441758981243551820180899010045052528910892432637, 556222500349083628750792911668379086104399463534898183365871029847714485, 1430009725688437081837786010369373666303115743644988400997380370434137966, 1348756909262472898689130791048079137260709879046965969522428936318337041, 147955972777038513149251979214766827104071235484042615207812511620367136, 1558128055596396598486851165346677673954733828361841009979002170900220453, 647802320846268913664180731745647182005001534858051148707691874236143989, 1295970226212643630812949429218264530326613200685247811960010181585356014, 1704566529464644844739857727665958701193111834963443443430601566150099780, 1685612534844092308536901445465011278946460023941595747037124675954029045, 426829862531928044770561977537943331343921364748501018315917684353783487, 1422657406070510752967346727320393929858178074227224098536543543337460634, 369639807280755520826576650549855018737976206423081176961190189062745482, 1293435618521127914495592173116187713067013594729867900061826653623215724, 1603742440407369077327155440774548921077283568257133872432164328658280680, 769170384784243112364855216926609722349267732682902316055477215414765179, 1139329406345144818196015633675955147193684448592702885572762273936046259, 1550015120670527735234558214011420564312691016196914562824664429508383501, 303634511493121213549572582689010310271858880789853149527258003197657367, 1244700208411973069323246045009509119096465069045000233341426684945978074, 371489588878748464739684346306755147611010126217835949732645825987164552, 591716274866864586959615425886996113095412419537523720770164701502601838, 999828201581942654958769571869289790182770729098962456815315657373185046, 904609704617652467227673924588394801273940932200426749196667754011531717, 1494476372680791236234288619260545364119291039905085865738826283634497355, 304442078957015527681921547129535180690405276739912833667492165127575927, 1160026594500095911705286824264598663370074394151795658895978542708569409, 120472769601148320211040975141305380807085361780627597412211555227748488, 503574112970046133140279045780034242916141706566012180514761574540237087, 1365822677319799384520097628839221626599213889022934946427544219647987118, 1543078152937622042983047868851260011891575265401182293125340624754211978, 620528904715306932331698322060770996474433583098963899463875793726332985, 1057187865640966949874244083734573970708492211726107680936768822829580606, 909496662307832408005470565634716951846850234983768887100850495121677296, 731790795060210162735380515900120020314048868001287117803453671991377570, 635937063855752101515232496262397379469536679668147978327016002305072142, 923272153799213058721550860958809435063930641052874706339222255990358670, 990497955754009077719573521262089529784860664812960309243537206266409190, 1240443010515845181014482056776523255292925485241671669473791159876546028, 1513422974623882140078025854911245705388563631389562401169577330780823442, 167187009938221560056080370102741734759127515915136632178166103562939230, 6626494665576649852846505859635436627510348419141330206254871004761047, 1650029393270954782046961322666037855467431541725665391982960467420263824, 255931699025788946574389006451537056812642580178245027026213221957076298, 840424675609053132613326722175682037831746055186982874441217863430307842, 25929609355305613275925418926819741105222528872284595393793811716855620, 1718722485248037037658803530864040354084411240493641122724449233048220011, 1583425990391276934921948013280728820682333671406809784662210565511420277, 1200398501796584706101092352047915828996561635025316854934139579051628614, 1592493651868951542083847884682608486169734873538723473677515057716512674, 1275600711923155827873895038888985164702100479969699039750572854872134331, 250930185777193279295271274918608825681660757636331340103747611415693286, 378949502405429999772810386125999846524925613344625824518069198251198684, 1020479902174401321188028436577600036452674004167432455182876941264046152, 1631718502003157712703961158814606646569009519864751030129141420388606852, 678919445022754683358285869912405050823365431998238285986696796984210022, 221525365247504818284642970357282039675787142742647333624360527697844954, 1752141579367271155211297250898040445774550366117118346999474841155386741, 1566288415277690792693841300282156935106395019220430523117166907796763893, 1603620611839189830705428492638417608608682177392719062580910461141108638, 600105810248525634282597416666258128606229514986701541360156136140549173, 218081063863007994768530474600288265241426059431509681280957504450476623, 251881924333774203832910004696758393629851114025800429292403783569844473, 1233811240080416485370016853538474292092822661314989152365689363395392713, 1674001516877851337411643853322844114307197639406323277736592908909257425, 790478397754270585356546704542332604771727450246319888963879842907680368, 1590866086375319108427204087995177225475833798021672202012459465206498012, 1039756679670412325207234428671384898380607647003080177655691561039424259, 1288887584732266155617901080691613971320601292761305423499267506807605696, 1709289970395359537592390609464977936502211890340177713398257631681315467, 434711263443451832659361951919140604512391458602228037762326935599389310, 1075431826724733355445998450511553827111367596582381050828963476879499740, 1052310494042442869107086089398566077588990793838993777387906384783788443, 74344382045983379924427196662015586071603985229588935843336797879414022]

        self._run_correctness_test(seed, e, expected_outputs)


    def test_vec1(self):
        e = 62010888751914997671799482329255879224336688873652957318511901048287904312729
        seed = 18342330105270810402
        expected_outputs = [683205848264760441991882654358788743401982788675583122720545194067021940, 1283638861640358774988807712437178829358283024194348087093686819729385824, 657743854749047563878837287113588033061224613029509634396649641782520983, 1232788213981545462760032544545319057616755913293763014566345986748579030, 181155490680916548550558726753344272941862268823237348644282448958483783, 1077922168130367285672508539128663583619621249272012507481907363607107446, 741833107456392621898238727226655814639278000923306819281628111514150100, 19149843711731851719739299588466105864902988930570305938125214577312964, 318368950349013375194490750469821201972080154550983605937515015838800629, 1294012076208953564442998428077637833770986082220962415065323951598370660, 1523814502163958073194472430706091566576613315929671567758619661846477077, 76518770821535610749203988884160233961321446984037733232477118788078203, 446846190043910998988884958851742392772346096709862349027183739446867747, 53971634034138328751726024693123289830171536907173764307413409396469824, 1362248691314828006158571115252038804836186612577748178568519702994719079, 1426327275263245371621053735132525009660139221212078237899019403704385565, 1068279642099072506048262468245057252784149323976925942647007628790633757, 1099950218365675754891675108099161263810375224450951696878030547400658318, 473310939862870859515006931423403397277051114394440059109164099533304141, 772775669067370635652055565983042385919756230497300180713949892381564, 1167803572710255677857327466334559615379255755341605428715347694892289460, 699344880479917655685163491358230944698174366644792641660617756550199716, 401911915906186465632594751381967813417673983548583255185457227715926297, 1663394519279028922982888759633261189585706125144065817837833077210819745, 71512663153794316661766034915222982999325684190951851961033385560538777, 693312778161184892084913610853433903151843432428549522507612805353591328, 1393067561798342678610496741567394738532620670923620469680163560216303737, 1560672132001285250755766176358830092302867020132242159910170013330321459, 1088370170216168625060296599952497166106307431459836181214146375807055758, 578065135947700874871352127958938722817924428450578420505654772265918265, 648176823762375906350528558962702630512890915795105496480108332372176850, 591618419060049947868952981214226262658325972194124049068339741189877340, 199517303563064268338723196142891954101038430697190859637061431509642017, 1354165130885114584439705150261441530195010887535343623218110622696262301, 837961367940053344224460410105105833760575001032296087839429880658912522, 462009247943270537591395534638840093520206167055909631874965842440743718, 827553709644716889881140062434853308633232570476495668459068873927991146, 541587877492504116468730616968221260083564552438480039080592812251377153, 1604544050178534685081605174087910023275081386159177105996669798375892338, 1134005122216008133950684556811802461468235648396026987507705491903936203, 693206871764273485235981642606006701432810786383449671866473745072466372, 449602344887344986779966346280579149502028273505634051784587508748066849, 615495515845532769891263882482895271298213666007465435508915746328469928, 787365653700116277278183201665703094930813845568074661245126109782992417, 1455629207328888331688769458907678671826175704076829655402843270511024227, 149012072013031094547998823233653089718010877372445736830765210686332891, 1053161965006767972268395438729844393724245047775201132359218658125431616, 853776002089819225352466943950819974701121910494220728478549605761271511, 1052044081019463568665524055954976655967769434724892800928866701171303218, 1199841600035779034871705356754974832060339249208855143325615861483301375, 1280820137297848834834668108574701258730551995945579326864724687806406255, 117634982753651240117520295476303895051820566449002527660777340139303944, 1064802642095354968046340736061059511670532298808371075393108136697609706, 1038467427995672742963992426270934642245533969681191995811315669573492490, 284360061424054066422887513382119695450303549470328440386265476205671699, 105433569898839517844271114481803920844405678063273456310442307942706467, 1571675722365706942884806505721129183808660177180954449380539589060146250, 1581693724770016952487187539497817744194943180389377852015404590332016147, 417041494438750552507897441847793733167242213553327660814919159098135950, 41013053022523118846109578079294766289149151081854225356041209148101875, 301314721353726040492533294883201417063789207538226496457322861409780236, 279609866287962550544702263267873512698651968602828902291965006254116713, 673201403067795170859166225555816798724796891086351334631998773038862795, 567242704302512414434427663466390831644057338171193359611319606800445283, 752278730611584380566450007487847190688766460479138310503042513835341378, 961568925400629930730791521853233290266368011205240829741134503984196945, 135628662645638098532911086427500814345392209672773164176685489188734231, 1347881805062495458357914483686154263726617491018581091712324349457997222, 995483285022963544621867735444057836181153633460321657840330623096993511, 446657726432599346378220775951721885211558338695505464291355939064402258, 426225597502562510231890426243841329479716213596840269855096053998312466, 1486290645657563542383858279997888129005320249704563559695047947353356872, 479376916538745334371676743874380719075383304696901073877241473584467178, 462087711665684650683914674723997723024479795495232485171098092912399838, 1525232159496474077275659588360073539676148477432816639682433853784199423, 345714533099312102939074055312585340991795654342513908212589141975610971, 261268827774376324206356338832021230995859119459505461880108389381491909, 992805642127454504283054297755385237136265070746162871233563025461700493, 182249734259516370263799884449541368436040768534319321052424873525061888, 128038774095968497774749755187032846653800609719130503074558038324472808, 843533020484015649821626979431342586201606256007023077004364641646203313, 50828589121596552233371989592419948089264533787712021033830915939724113, 1330024808092442617441656322076559420664898601555369581077617435725293858, 888356734094556776294370042511709550808440250711236274676247539361045113, 1532654032187100691096635749790149544990337386538929424557422165406616955, 673841148402129857852709270853860656615451944136028107583155612094510344, 184506813353133038987434353645242749158864047059813128952939772658253077, 1586227145562761822051554077071702738282514590639462026508779977211189175, 651007472450579214343020584401723939850739888278788038841831759105309737, 1689761150884961671441858190680712449138324578742756805209558716988918707, 1687707981707088936384717004652799783450049134851481401733624490955093150, 526563340962773993212857128452853510828345593105427251629607577629956425, 950201009878460225022684046117508192750731574023625003261545701857339315, 242284628974603418878843077354914368281399866566104466580256226463888918, 1004368863478454154262900773432337060789831241965805624999058095688868185, 881568929515562114361034854339462896062135722163860146226490934554383662, 55217822805778377209161841759811841802898199665092199805576177711080620, 769654245000218143848734025561449746958776066938249342858081946365561510, 770140359896164380685488328965507534575386150533671649623348110851956434, 742635106744447557399635603058498439031137787482912767844866363825061752]

        self._run_correctness_test(seed, e, expected_outputs)


    def test_vec2(self):
        e = 463539773449426982977445513884422579299138225062541531114216814411394385795
        seed = 1752127567141660693
        expected_outputs = [1467441072376545428229012857931419956001986031697748126760861104076782848, 201212526843486400454446399411217186968938876191541328123847733952954562, 528449716523421089304241597776529595760415806359990115335384027307203521, 750911101649645987298351198293065470814840740822014783266530880508720028, 1462111211741067604828194930841178655999153319787868277169017652890592708, 148106483457621450789287298091095450510329073062203070419714994551213378, 818574282433096402716392182571944149927667672391008237146330310335804458, 609973382480057092322328446926148290684301619543741581047054768693417583, 1724517296496065516834207053651222713107149590963001315689548641354648682, 839787442715983721672633696632255082681874066898332135630837593216481616, 94178888395052560669619307907726332616261175980186726536009212196686939, 1497849276077644908859579803686882068173047805634156413468303379859050752, 81131459310137598368370508008711609282740953871336397527288834922865355, 1025306357960335117403803846630063976901797323140961575393796152529386518, 94938577785484285412409060741543150415957739641069659202774142447617258, 1069662429809214288205161986029644707560634605171898564001593675757446837, 1520164086029670818492212688078410918217129766507630819850815598182097090, 1063852015926830807496794462129041082169126309933225366391833684545802773, 1136423739940012492005817864624510024419549049006710311112026601847164225, 1272929536204687176567419616840081337464299916596522392468498180363952518, 1212566423215918078139055732936664038461813138331698950182979285002890613, 462372587673610834972440747357667531810959497372471215282214487352488439, 1130954909198250076550058941015529584188347357883231512832117867868360316, 24481273493610336285665869818638230007581608601366237103829933457462533, 669183646512431332626407121967328158510059414042832638037506739710926026, 1461359071866686113656895288268938871400482433522767623225911488553820721, 577098547304942516806350380788759829912417033851848598005552263514313311, 408130952869321342244118032918183461240136588802928743640896805605060067, 291550059714440275040886333229030003738109552502463848187491740585223632, 1120990363252153372171026388193697239922317807137089748701676770421989267, 1174330734929004004296653791016457464873217219366408360932227986875106321, 1027992486050320124695667038050340857606625220004130261314675101535646186, 412426156443927474723163199975470110987908785566367856685543982678822447, 874327071451749079192086461532689108918958086774215401134001112976760929, 777196598346202738916661869280188805625933989471979922287167653721377302, 804620026604007806219653256172832557704910163884803670524307552541417602, 1392598902109275447863467322634062975770760076984814997336617157104137522, 832598338997435667863864451695625399536909145442088499367896415960961868, 1165711247055706361568444734137165522321335129805366014105566219830934191, 457485891431266870704854100017071311758236136240403822064090968618488403, 951295085922467313834533559991353798350412096101974176273006168323362818, 1230695413693385911117239548519824191997521701131693420862467967340506123, 1059037843277859717614835290660704682474004790262553417751374194722684387, 1211440902476171204288521245016284836185703858335646363876196318850075472, 1332352625670637278586310235871369585096877443314559915327307514964998222, 162930708992845940746520668386123126499150159813981189637286827772069713, 653658065106215417373704287130416183601519657881469007341713429694910432, 976521144612655063248868281430073562123647034674295748046804477789796364, 983535296864149624003955768833989397413702463150115879179201187587924213, 61194256640238283395362643304564098790825210738522250510475164118754087, 235776380167359394572951888246762004901003463522897905715313750945035296, 1231280087812981942337757530607840421487268766232240913450008494968129928, 276698825047864485964517660755199583650547708276474489199091825745658911, 1226302303938394140254861157266505952996190261485708233183911918564000721, 523418900504375046426444268375140784512750257522335340804639086228810681, 833454795578907341359205743897897021775284694457692248318774554299637013, 1341400672795352556103940101491800372317248271314026323671441045341923661, 1342879272930432477871968198555310309457113529396580497204178630374038598, 1403531680072996121167041783808487417615899513136210901290503959724386782, 1613157225266669178474867258449762247358876985548406281051990151854528841, 1541789341861243336696835270017951105188183962717985612823692258097213334, 342112392589748909813805172338455664675977495279357099896834578726239788, 251648118356117266824698695423120259998158166363428495027252286385433090, 827198370466420891860602284146850997453369902437257084449805264344926193, 491497499696701187819195850792582081704681702460335813242410067587092910, 750366150911433082996252854498382381253685022445472712973580665133805316, 168563464217316505330754123615227852275208304181103576298262733944369860, 850762972899159287473436589885644640910961899249722128944420020609492708, 54136306394602110474450196642861919882458005960901957986314780404138792, 784394440388835023029733277867991883675609777240458767352911907185309843, 1114439102455743460258844332749882122866178696348747570635108935757105575, 1538519390916742568695243208092611880543651517581590822829066331711040888, 312166592132609279736657353890153178110635036415167160624982599197294073, 299602562046283199674631045696894005288986710702818547146319814394929700, 624676509803324224506174290831106670602086412351497747643382187893162906, 534544418730398483594105623497916914602969057802994462852503991211794184, 1531660664823510837787008380864532568353123855132749336786404988783264481, 156814403827139346194142757038946744218867537761233306933363122147164389, 1628743853966542743265756527661413092373989324100799358204946413890323524, 46260390444781228356724019860685884342010703825418558537026936752487121, 639838398155065409918003594996838146599394549326953060543518993072958354, 1202775732032667180764401408795465321179754145152519010859199507228198541, 616293659828962693916198554520477901179241398743145068192831692920880372, 980584311891025351033391570500284968815921580864745159737353699982983496, 1750630829676579553169240429830347684436234241655854433740489823597248130, 804044866808282605276636083459065868700568722729372920027044440482394309, 418793617943327879565204709567527950050158422247999452482300427547312146, 108175572595032197439475828066578994866202217332050154851071038741509561, 1036944339469027402243104859399863612383849860007993556483757468214008760, 1360269039823796181222736639684058543332792098378371153995001906794478611, 287016418631712506590167038125071346413122539021691422050408346859461047, 1463606213914551076884122704974262440745468447069790155554090590900252217, 440496844667189797739936980172177213387526901153988691340795668677395763, 437881494864822646735206327009616869232363264352192513533146316742834238, 1425043191801534512382493314833847612810683700274632136837628071935963476, 240321769273813975060928581492487793743004941910549875869798870371375431, 1251940720715193895922565133761865222536813601671116473320646027941326800, 629444592232886703096671395468262970438972209944609075830993504209925236, 1716336721453376152822621040467954681194658330529525537281850500426727809, 490674164985472086221934636016314452698862611261450508067447401491857508]

        self._run_correctness_test(seed, e, expected_outputs)
